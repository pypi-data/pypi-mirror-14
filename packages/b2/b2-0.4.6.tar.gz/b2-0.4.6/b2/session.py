######################################################################
#
# File: b2/raw_api.py
#
# Copyright 2016 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

import functools

from .exception import (InvalidAuthToken)


class B2Session(object):
    """
        Facade that supplies the correct api_url and account_auth_token to methods
        of underlying raw_api and reauthorizes if necessary
    """

    def __init__(self, account_info, raw_api):
        self.account_info = account_info  # for reauthorization
        self.raw_api = raw_api

    def __getattr__(self, name):
        f = getattr(self.raw_api, name)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            auth_failure_encountered = False
            while 1:
                api_url = self.account_info.get_api_url()
                account_auth_token = self.account_info.get_account_auth_token()
                try:
                    return f(api_url, account_auth_token, *args, **kwargs)
                except InvalidAuthToken:
                    if not auth_failure_encountered:
                        auth_failure_encountered = True
                        reauthorization_success = self.account_info.authorize_automatically()
                        if reauthorization_success:
                            continue
                        # TODO: exception chaining could be added here
                        #       to help debug reauthorization failures
                    raise

        return wrapper
