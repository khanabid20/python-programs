#!/usr/bin/env python3
import jenkins
import time, datetime
import sys
import os, json

'''
Pre-req:
    `python-jenkins` module
    To install it run 'pip install python-jenkins'

Description:
    This script takes couple of environment variables and trigger a build, wait for the status and exit.
    There is a flag to turn ON or OFF printing of jenkins console log on to the terminal.

How to Run:
    export JENKINS_URL=https://jenkins.example.com
    ... rest of the environment variables
    ./<script-name>
'''

# Get environment variables
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_JOB_NAME = os.getenv('JENKINS_JOB_NAME')
JENKINS_PARAMETERS = os.getenv('JENKINS_PARAMETERS', {"key":"value"})
JENKINS_API_TOKEN = os.getenv('JENKINS_API_TOKEN',"s0m3th!ngC0mpl3x")
JENKINS_USERNAME = os.getenv('JENKINS_USERNAME')
JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD',JENKINS_API_TOKEN)
# Flag to turn on/off printing of jenkins log onto the console
JENKINS_CONSOLE_OUTPUT=os.getenv('JENKINS_CONSOLE_OUTPUT',False)

class DevOpsJenkins:
    def __init__(self):
        self.jenkins_server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        print ("Jenkins Version: {}".format(version))
        print ("Jenkins User: {}".format(user['id']))

    def build_job(self):
        next_build_number = self.jenkins_server.get_job_info(JENKINS_JOB_NAME)['nextBuildNumber']
        self.jenkins_server.build_job(JENKINS_JOB_NAME, parameters=json.loads(JENKINS_PARAMETERS), token=JENKINS_API_TOKEN)
        # time.sleep(10)
        # build_info = self.jenkins_server.get_build_info(name, next_build_number)
        # return build_info
        # return build_info['queueId']
        return next_build_number
    
    def poll_status(self, next_build_number):
        job_url_shown = False
        while True:           
            time.sleep(15)
            self.build_info = self.jenkins_server.get_build_info(JENKINS_JOB_NAME, next_build_number)
            # print(build_info)
            if self.build_info["result"] is None:
                if not job_url_shown:
                    print(f"\nRunning: {self.build_info['url']}\n")
                    job_url_shown = True
                print(".", end="", flush=True)
            else:
                if self.build_info['result'] == 'SUCCESS':
                    print(self.build_info['result'])
                    return 0
                else:
                    print(self.build_info['result'])
                    return 1
    
    def print_console_output(self, next_build_number):
        print('------------------  BEGIN - JENKINS CONSOLE OUTPUT ------------------')
        print(self.jenkins_server.get_build_console_output(JENKINS_JOB_NAME, next_build_number))
        print('------------------    END - JENKINS CONSOLE OUTPUT ------------------')
        pass


if __name__ == "__main__":
    # print(datetime.datetime.now())

    jenkins_obj = DevOpsJenkins()
    next_build_number = jenkins_obj.build_job()
    exit_code = jenkins_obj.poll_status(next_build_number)
    
    # print(datetime.datetime.now())

    # Print jenkins console log
    if JENKINS_CONSOLE_OUTPUT:
        jenkins_obj.print_console_output(next_build_number)
    
    print(f"\nJenkins Console Url: {jenkins_obj.build_info['url']}console\n")

    sys.exit(exit_code)
