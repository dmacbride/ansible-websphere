#!/usr/bin/python

#
# Author: David MacBride <dmacbride@gmail.com.
#
# Get info about a WAS application server

import os

def main():

    # Read arguments
    module = AnsibleModule(
        argument_spec = dict(
            was_install_dir  = dict(required=True),
            was_profile_name = dict(required=True)
        )
    )

    was_install_dir = module.params['was_install_dir']
    was_profile_name  = module.params['was_profile_name']

    was_profile_dir = was_install_dir + "/profiles/" + was_profile_name

    # Input validation
    if not os.path.exists(was_install_dir):
        module.fail_json(msg="The specified path "+was_install_dir+" does not exist")
    if not os.path.exists(was_profile_dir):
        module.fail_json(msg="The WAS profile directory " + was_profile_dir + " does not exist")

    child = subprocess.Popen([was_profile_dir + "/bin/wsadmin.sh -lang jython -conntype NONE -c \"AdminConfig.list('Server')\""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = child.communicate()
    if child.returncode != 0:
        module.fail_json(msg="Wsadmin command to find servername failed", stdout=stdout_value, stderr=stderr_value)

    module.exit_json(changed=False, msg="Run successfully")


# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
