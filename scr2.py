#!/usr/bin/env python3

import os

bash_command = ["dig google.com | grep google.com. ","dig drive.google.com | grep google.com.","dig mail.google.com | grep google.com" ]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('ANSWER SECTION') != 0:
        prepare_result = result.replace('\tANSWER SECTION   ', '')
        print(prepare_result)

