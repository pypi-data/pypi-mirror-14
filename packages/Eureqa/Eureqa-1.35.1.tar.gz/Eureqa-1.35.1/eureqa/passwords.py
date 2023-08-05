# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Nutonian Inc nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NUTONIAN INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import getpass
import json
import os
import os.path
import sys

def _get_password_file():
    # store password file outside of the source directory
    PASSWORD_FILE = '.eureqa_passwd'
    path = os.path.expanduser("~")
    return path + '/' + PASSWORD_FILE


def _load_passwords():
    try:
        with open(_get_password_file(), 'rb') as f:
            return json.load(f)
    except:
        return {}


def _find_login(data, url, username=None):
    if url not in data: return None

    def login_timestamp(login):
        try:
            return datetime.datetime(login['last_used'])
        except:
            return datetime.datetime(2000, 1, 1)

    max_date = None
    max_date_i = None
    for i, login in enumerate(data[url]):
        if username and login['username'] != username:
            continue
        date = login_timestamp(login)
        if not max_date or date > max_date:
            max_date = date
            max_date_i = i
    return max_date_i


def _prompt_username():
    username = raw_input('ENTER USERNAME: ')
    if not username:
        raise Exception('Login cancelled by user')
    return username


def _prompt_password_spyder():
    return raw_input('ENTER PASSWORD: ').encode('base64')


def _prompt_password():
    if any('SPYDER' in name for name in os.environ) or 'pythonw.exe' in sys.executable:
        password = _prompt_password_spyder()
    else:
        password = getpass.getpass('ENTER PASSWORD: ').encode('base64')
    if not password: raise Exception('Login cancelled by user')
    return password

def _prompt_one_time_password():
    password = raw_input('ENTER ONE_TIME PASSWORD SENT BY SMS: ')
    if not password: raise Exception('Login cancelled by user')
    return password


### MAIN FUNCTIONALITY: ###

def store_login(url, login):
    """Saves login credentials to they are used automatically next time.
       Credentials are saved to a file your home directory.
    """
    data = _load_passwords()
    if url not in data: data[url] = []
    login['last_used'] = str(datetime.datetime.now())
    index = _find_login(data, url, login['username'])
    if index is None:
        data[url].append(login)
    else:
        data[url][index] = login
    with open(_get_password_file(), 'wb') as f:
        json.dump(data, f, indent=4, default=str)


def get_login(url, username=None, password=None, key=None, force_prompt=False, two_factor_auth=False):
    """Returns (username, password) for a Eureqa SaaS url and prompts user for 
       credentials if not found. Passwords should be base64 encoded.
       If no username is provided the function returns the most recently used login.
       If force_prompt is True the user will always be prompted to enter credentials.
    """
    data = _load_passwords()

    index = _find_login(data, url, username)
    login = data[url][index] if index is not None and (username is None or password is None) else {'username': username, 'password': password}
    if key:
        login['key'] = key

    ask_username = force_prompt or not login['username']
    ask_password = (force_prompt or not login['password']) and not key

    if ask_username or ask_password: print('PLEASE LOGIN,')
    if ask_username:
        login['username'] = _prompt_username()
    elif ask_password:
        print('LOGGING IN WITH USERNAME: ' + login['username'])
    if ask_password: login['password'] = _prompt_password()

    if two_factor_auth: login['one_time_password'] = _prompt_one_time_password()

    return login
