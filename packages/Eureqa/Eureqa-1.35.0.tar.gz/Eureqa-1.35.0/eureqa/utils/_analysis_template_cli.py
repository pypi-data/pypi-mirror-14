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

"""
Internal module.  For use by the analysis_template command-line tools.
"""

import importlib
import warnings
import textwrap
import getpass
import json
import os

from eureqa.analysis_templates.parameters import Parameters

EUREQA_CONFIG_FILE = "eureqa_config.json"


DESCRIPTION = textwrap.dedent("""\
    This script is used to upload, run, and otherwise work locally with
    Analysis Templates.

    The first time this script is run, all argument values (other than the
    password) will be saved to a file named '%s' in the
    specified module directory.  Subsequent runs against a module will use the
    the options saved in that file by default so that you don't need to pass
    them in again.
    """ % EUREQA_CONFIG_FILE)

def add_module_args(parser):
    """ Arguments for describing the module to upload and run """

    module_args = parser.add_argument_group("Module Arguments")
    module_args.add_argument("module_dir",
                             help="Directory for module to upload")

def add_server_args(parser):
    """ Arguments for connecting to the Eureqa server """

    server_args = parser.add_argument_group("Server Connection Arguments")
    server_args.add_argument("-u", "--username",
                             help="Username for Eureqa server")
    server_args.add_argument("-p", "--password",
                             help="Password for Eureqa server",
                             default='')
    server_args.add_argument("-k", "--api_key",
                             help="API Key for Eureqa server",
                             default='')
    server_args.add_argument("-o", "--organization",
                             help="Organization to upload the analysis template to (default: 'root')",
                             default=None)
    server_args.add_argument("--url",
                             help="URL to the Eureqa server (default: 'http://localhost:10002')",
                             default=None)
    server_args.add_argument("--verify_ssl_certificate",
                             choices=['true', 'false'],
                             help="Verify SSL certificate authenticity while connecting to server",
                             default='true')

## Args that are in either template_args or local_template_args
## Each may ignore saved parameters intended for the other
SHARED_ARGS = {"name", "description", "id", "parameter_values"}

def add_template_args(parser):
    """ Arguments for configuring the new template on the server """

    template_args = parser.add_argument_group("Template Configuration Arguments")
    template_args.add_argument("-n", "--name",
                               help="Name of the template to create (default: 'Example Template')",
                               default=None)
    template_args.add_argument("-d", "--description",
                               help="Description of the template to create (optional)",
                               default=None)
    template_args.add_argument("--id",
                               help="ID of template to update.  Optional; if omitted, will create a new template.",
                               default=None)

def add_local_template_args(parser):
    """ Arguments to be passed to the new template when running the template locally """

    template_args = parser.add_argument_group("Template Configuration Arguments")
    template_args.add_argument("--parameter-values",
                               help="JSON string describing the values for the Parameters to be passed to the template at runtime",
                               type=json.loads,
                               dest="parameter_values",
                               default="[]")

def add_script_args(parser):
    """ Arguments that control details of the script's behavior """

    script_args = parser.add_argument_group("Script Usage Flags")
    script_args.add_argument("-q", "--quiet",
                             help="Only print the ID of the new analysis template to stdout.  Don't prompt for input on stdin.",
                             action='store_true')
    script_args.add_argument("--no-save",
                             help="Don't save arguments as %s" % os.path.join('[module_dir]', EUREQA_CONFIG_FILE),
                             dest="save", action='store_false')
    script_args.add_argument("--save-credentials",
                             help="Save login information to the Eureqa API credential store (not encrypted)",
                             dest="save_credentials", action='store_true')

def merge_defaults_from_json(module_dir, args):
    """ Read in default argument values from a user-created JSON config file """

    # 'hardcoded_defaults' are default values for fields that
    # want something fancier than None.
    # We can't use argparse for them because we want a semantic
    # difference between an argument's default value and
    # an argument that has been explicitly set to a value that
    # happens to equal its default.
    hardcoded_defaults = {
        'organization': 'root',
        'url': 'http://localhost:10002',
        'name': 'Example Template'
        }
    # Some defaults are legitimately None.  Import them.
    default_values = {k: v for k, v in args.__dict__.iteritems() if v is None}
    default_values.update(hardcoded_defaults)

    defaults_file = os.path.join(module_dir, EUREQA_CONFIG_FILE)

    cmdline_args = {k: v for k, v in args.__dict__.iteritems() if v is not None and v != []}

    if not os.path.isfile(defaults_file):
        json_conf = {}
    else:
        ## Load from JSON file
        try:
            with open(defaults_file) as f:
                json_conf = json.load(f)

                # Undo un-wrapping in write_defaults_to_json()
                if 'parameter_values' in json_conf:
                    json_conf['parameter_values'] = { 'parameters': json_conf['parameter_values'] }

        except Exception, e:
            warnings.warn("Error parsing configuration file: '%s'" % str(e))
            json_conf = {}  ## No config file for now

    argnames = set(args.__dict__.keys())

    ## Check for unrecognized stuff in the JSON
    unrecognized_keys = set(json_conf.keys()).difference(argnames).difference(SHARED_ARGS)
    if unrecognized_keys != set():
        warnings.warn("Unrecognized keys in %s: %s" % (EUREQA_CONFIG_FILE, ', '.join(unrecognized_keys)))

    conf = default_values
    conf.update(json_conf)
    conf.update(cmdline_args)

    return conf


def clean_and_populate_params(params, prompt):
    """ Make sure we have all requred params.  Prompt the user for missing values. """

    ## argparse should guarantee that this exists
    assert params['module_dir']
    assert params['organization']

    params['module_dir'] = os.path.abspath(params['module_dir'])

    if not params.get('username', None):
        if not prompt:
            fail_no_prompt('--username')
        params['username'] = raw_input("Username: ")

    if not params.get('url', None):
        if not prompt:
            fail_no_prompt('--url')
        params['url'] = raw_input("RPC URL: ")

def fail_no_prompt(missing_arg):
    """ Error out and exit if we're missing an arg and can't prompt for it """

    raise RuntimeError, "Error:  Missing argument '%s'" % missing_arg

def module_name_from_module_dir(module_dir):
    return os.path.basename(module_dir)

def get_parameters_from_module(module_name):
    mod = importlib.import_module(module_name)
    return getattr(mod, 'template_parameters', Parameters)()

def write_defaults_to_json(params, module_dir):
    """ Write computed arguments to the Eureqa JSON file for this module """

    params = dict(params)  ## Make a copy, to avoid surprises in the caller

    ## Delete parameters that we don't want to persist

    # Saved through Eureqa's credentials store instead
    if 'password' in params:
        del params['password']

    # One-time command-line behavior
    if 'quiet' in params:
        del params['quiet']
    if 'save' in params:
        del params['save']
    if 'save_credentials' in params:
        del params['save_credentials']
    if 'verify_ssl_certificate' in params:
        del params['verify_ssl_certificate']

    # Redundant (we're writing to a file located at this path)
    if 'module_dir' in params:
        del params['module_dir']

    if 'parameter_values' in params:
        ## Un-wrap 'parameter_values' serialization format for easier-to-read storage
        try:
            params['parameter_values'] = params['parameter_values']['parameters']
        except:
            pass  ## Don't know what you're up to but apparently the server liked it?

    try:
        with open(os.path.join(module_dir, EUREQA_CONFIG_FILE), "w") as f:
            json.dump(params, f, indent=4, sort_keys=True)
    except Exception, e:
        warnings.warn("Unable to save settings to '%s': '%s'" % (EUREQA_CONFIG_FILE, str(e)))
