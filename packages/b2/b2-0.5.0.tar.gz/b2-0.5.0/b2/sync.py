######################################################################
#
# File: b2/sync.py
#
# Copyright 2016 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

import os
import sys
import threading
import time
from abc import (ABCMeta, abstractmethod)

import six


class SyncReport(object):
    """
    Handles reporting progress for syncing.

    Prints out each file as it is processed, and puts up a sequence
    of progress bars.

    The progress bars are:
       - Step 1/1: count local files
       - Step 2/2: compare file lists
       - Step 3/3: transfer files

    This class is THREAD SAFE so that it can be used from parallel sync threads.
    """

    STATE_LOCAL = 'local'
    STATE_COMPARE = 'compare'
    STATE_TRANSFER = 'transfer'
    STATE_DONE = 'done'

    def __init__(self):
        self.start_time = time.time()
        self.state = 'local'
        self.local_file_count = 0
        self.compare_count = 0
        self.total_transfer_files = 0  # set in end_compare()
        self.total_transfer_bytes = 0  # set in end_compare()
        self.transfer_files = 0
        self.transfer_bytes = 0
        self.current_line = ''
        self.lock = threading.Lock()
        self._update_progress()

    def close(self):
        with self.lock:
            if self.state != self.STATE_DONE:
                self._print_line('', False)

    def print_completion(self, message):
        """
        Removes the progress bar, prints a message, and puts the progress
        bar back.
        """
        with self.lock:
            self._print_line(message, True)
            self._update_progress()

    def _update_progress(self):
        rate = int(self.transfer_bytes / (time.time() - self.start_time))
        if self.state == self.STATE_LOCAL:
            message = ' count: %d files   compare: %d files   transferred: %d files   %d bytes   %d B/s' % (
                self.local_file_count, self.compare_count, self.transfer_files, self.transfer_bytes,
                rate
            )
        elif self.state == self.STATE_COMPARE:
            message = ' compare: %d/%d files   transferred: %d files   %d bytes   %d B/s' % (
                self.compare_count, self.local_file_count, self.transfer_files, self.transfer_bytes,
                rate
            )
        elif self.state == self.STATE_TRANSFER:
            message = ' compare: %d/%d files   transferred: %d/%d files   %d/%d bytes   %d B/s' % (
                self.compare_count, self.local_file_count, self.transfer_files,
                self.total_transfer_files, self.transfer_bytes, self.total_transfer_bytes, rate
            )
        else:
            message = ''
        self._print_line(message, False)

    def _print_line(self, line, newline):
        """
        Prints a line to stdout.

        :param line: A string without a \r or \n in it.
        :param newline: True if the output should move to a new line after this one.
        """
        if len(line) < len(self.current_line):
            line += ' ' * (len(self.current_line) - len(line))
        sys.stdout.write(line)
        if newline:
            sys.stdout.write('\n')
            self.current_line = ''
        else:
            sys.stdout.write('\r')
            self.current_line = line
        sys.stdout.flush()

    def update_local(self, delta):
        """
        Reports that more local files have been found.
        """
        with self.lock:
            assert self.state == self.STATE_LOCAL
            self.local_file_count += delta
            self._update_progress()

    def end_local(self):
        """
        Local file count is done.  Can proceed to step 2.
        """
        with self.lock:
            assert self.state == self.STATE_LOCAL
            self.state = self.STATE_COMPARE
            self._update_progress()

    def update_compare(self, delta):
        """
        Reports that more files have been compared.
        """
        with self.lock:
            self.compare_count += delta
            self._update_progress()

    def end_compare(self, total_transfer_files, total_transfer_bytes):
        with self.lock:
            assert self.state == self.STATE_COMPARE
            self.state = self.STATE_TRANSFER
            self.total_transfer_files = total_transfer_files
            self.total_transfer_bytes = total_transfer_bytes
            self._update_progress()

    def update_transfer(self, file_delta, byte_delta):
        with self.lock:
            self.transfer_files += file_delta
            self.transfer_bytes += byte_delta
            self._update_progress()


def sample_sync_report_run():
    sync_report = SyncReport()

    for i in six.moves.range(20):
        sync_report.update_local(1)
        time.sleep(0.2)
        if i == 10:
            sync_report.print_completion('transferred: a.txt')
        if i % 2 == 0:
            sync_report.update_compare(1)
    sync_report.end_local()

    for i in six.moves.range(10):
        sync_report.update_compare(1)
        time.sleep(0.2)
        if i == 3:
            sync_report.print_completion('transferred: b.txt')
        if i == 4:
            sync_report.update_transfer(25, 25000)
    sync_report.end_compare(50, 50000)

    for i in six.moves.range(25):
        if i % 2 == 0:
            sync_report.print_completion('transferred: %d.txt' % i)
        sync_report.update_transfer(1, 1000)
        time.sleep(0.2)

    sync_report.close()


@six.add_metaclass(ABCMeta)
class AbstractAction(object):
    """
    An action to take, such as uploading, downloading, or deleting
    a file.  Multi-threaded tasks create a sequence of Actions, which
    are then run by a pool of threads.

    An action can depend on other actions completing.  An example of
    this is making sure a CreateBucketAction happens before an
    UploadFileAction.
    """

    def __init__(self, prerequisites):
        """
        :param prerequisites: A list of tasks that must be completed
         before this one can be run.
        """
        self.prerequisites = prerequisites
        self.done = False

    def run(self):
        for prereq in self.prerequisites:
            prereq.wait_until_done()
        self.do_action()
        self.done = True

    def wait_until_done(self):
        # TODO: better implementation
        while not self.done:
            time.sleep(1)

    @abstractmethod
    def do_action(self):
        """
        Performs the action, returning only after the action is completed.

        Will not be called until all prerequisites are satisfied.
        """


class B2UploadAction(AbstractAction):
    def __init__(self, full_path, file_name, mod_time):
        self.full_path = full_path
        self.file_name = file_name
        self.mod_time = mod_time

    def do_action(self):
        raise NotImplementedError()

    def __str__(self):
        return 'b2_upload(%s, %s, %s)' % (self.full_path, self.file_name, self.mod_time)


class B2DownloadAction(AbstractAction):
    def __init__(self, file_name, file_id):
        self.file_name = file_name
        self.file_id = file_id

    def do_action(self):
        raise NotImplementedError()

    def __str__(self):
        return 'b2_download(%s, %s)' % (self.file_name, self.file_id)


class B2DeleteAction(AbstractAction):
    def __init__(self, file_name, file_id):
        self.file_name = file_name
        self.file_id = file_id

    def do_action(self):
        raise NotImplementedError()

    def __str__(self):
        return 'b2_delete(%s, %s)' % (self.file_name, self.file_id)


class LocalDeleteAction(AbstractAction):
    def __init__(self, full_path):
        self.full_path = full_path

    def do_action(self):
        raise NotImplementedError()

    def __str__(self):
        return 'local_delete(%s)' % (self.full_path)


class FileVersion(object):
    """
    Holds information about one version of a file:

       id - The B2 file id, or the local full path name
       mod_time - modification time, in seconds
       action - "hide" or "upload" (never "start")
    """

    def __init__(self, id_, mod_time, action):
        self.id_ = id_
        self.mod_time = mod_time
        self.action = action

    def __repr__(self):
        return 'FileVersion(%s, %s, %s)' % (repr(self.id_), repr(self.mod_time), repr(self.action))


class File(object):
    """
    Holds information about one file in a folder.

    The name is relative to the folder in all cases.

    Files that have multiple versions (which only happens
    in B2, not in local folders) include information about
    all of the versions, most recent first.
    """

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions

    def latest_version(self):
        return self.versions[0]

    def __repr__(self):
        return 'File(%s, [%s])' % (self.name, ', '.join(map(repr, self.versions)))


@six.add_metaclass(ABCMeta)
class AbstractFolder(object):
    """
    Interface to a folder full of files, which might be a B2 bucket,
    a virtual folder in a B2 bucket, or a directory on a local file
    system.

    Files in B2 may have multiple versions, while files in local
    folders have just one.
    """

    @abstractmethod
    def all_files(self):
        """
        Returns an iterator over all of the files in the folder, in
        the order that B2 uses.

        No matter what the folder separator on the local file system
        is, "/" is used in the returned file names.
        """

    @abstractmethod
    def folder_type(self):
        """
        Returns one of:  'b2', 'local'
        """

    def make_full_path(self, file_name):
        """
        Only for local folders, returns the full path to the file.
        """
        raise NotImplementedError()


class LocalFolder(AbstractFolder):
    """
    Folder interface to a directory on the local machine.
    """

    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.relative_paths = self._get_all_relative_paths(self.root)

    def folder_type(self):
        return 'local'

    def all_files(self):
        for relative_path in self.relative_paths:
            yield self._make_file(relative_path)

    def make_full_path(self, file_name):
        return os.path.join(self.root, file_name.replace('/', os.path.sep))

    def _get_all_relative_paths(self, root_path):
        """
        Returns a sorted list of all of the files under the given root,
        relative to that root
        """
        result = []
        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                relative_path = full_path[len(root_path) + 1:]
                result.append(relative_path)
        return sorted(result)

    def _make_file(self, relative_path):
        full_path = os.path.join(self.root, relative_path)
        mod_time = os.path.getmtime(full_path)
        slashes_path = '/'.join(relative_path.split(os.path.sep))
        version = FileVersion(full_path, mod_time, "upload")
        return File(slashes_path, [version])


def next_or_none(iterator):
    """
    Returns the next item from the iterator, or None if there are no more.
    """
    try:
        return six.advance_iterator(iterator)
    except StopIteration:
        return None


def zip_folders(folder_a, folder_b):
    """
    An iterator over all of the files in the union of two folders,
    matching file names.

    Each item is a pair (file_a, file_b) with the corresponding file
    in both folders.  Either file (but not both) will be None if the
    file is in only one folder.
    :param folder_a: A Folder object.
    :param folder_b: A Folder object.
    """
    iter_a = folder_a.all_files()
    iter_b = folder_b.all_files()
    current_a = next_or_none(iter_a)
    current_b = next_or_none(iter_b)
    while current_a is not None or current_b is not None:
        if current_a is None:
            yield (None, current_b)
            current_b = next_or_none(iter_b)
        elif current_b is None:
            yield (current_a, None)
            current_a = next_or_none(iter_a)
        elif current_a.name < current_b.name:
            yield (current_a, None)
            current_a = next_or_none(iter_a)
        elif current_b.name < current_a.name:
            yield (None, current_b)
            current_b = next_or_none(iter_b)
        else:
            assert current_a.name == current_b.name
            yield (current_a, current_b)
            current_a = next_or_none(iter_a)
            current_b = next_or_none(iter_b)


def make_file_sync_actions(
    sync_type, source_file, dest_file, source_folder, dest_folder, history_days
):
    """
    Yields the sequence of actions needed to sync the two files
    """
    source_mod_time = 0
    if source_file is not None:
        source_mod_time = source_file.latest_version().mod_time
    dest_mod_time = 0
    if dest_file is not None:
        dest_mod_time = dest_file.latest_version().mod_time
    if dest_mod_time < source_mod_time:
        if sync_type == 'local-to-b2':
            yield B2UploadAction(
                dest_folder.make_full_path(source_file.name), source_file.name, source_mod_time
            )
        else:
            yield B2DownloadAction(source_file.name, source_file.latest_version().id_)
    if source_mod_time == 0 and dest_mod_time != 0:
        if sync_type == 'local-to-b2':
            yield B2DeleteAction(dest_file.name, dest_file.latest_version().id_)
        else:
            yield LocalDeleteAction(dest_file.latest_version().id_)
    # TODO: clean up file history in B2
    # TODO: do not delete local files for history_days days


def make_folder_sync_actions(source_folder, dest_folder, history_days):
    """
    Yields a sequence of actions that will sync the destination
    folder to the source folder.
    """
    source_type = source_folder.folder_type()
    dest_type = dest_folder.folder_type()
    sync_type = '%s-to-%s' % (source_type, dest_type)
    if (source_folder.folder_type(), dest_folder.folder_type()) not in [
        ('b2', 'local'), ('local', 'b2')
    ]:
        raise NotImplementedError("Sync support only local-to-b2 and b2-to-local")
    for (source_file, dest_file) in zip_folders(source_folder, dest_folder):
        for action in make_file_sync_actions(
            sync_type, source_file, dest_file, source_folder, dest_folder, history_days
        ):
            yield action


def sync_folders(source, dest, history_days):
    """
    Syncs two folders.  Always ensures that every file in the
    source is also in the destination.  Deletes any file versions
    in the destination older than history_days.
    """
