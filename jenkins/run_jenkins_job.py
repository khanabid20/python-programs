#!/usr/bin/python
import jenkins
import time
import sys
# It comes with pip module python-jenkins
# use pip to install python-jenkins

# Jenkins Authentication URL
JENKINS_URL = "<SERVER_URL>"
JENKINS_USERNAME = "<USERNAME>"
JENKINS_PASSWORD = "<API_TOKEN>"

NAME_OF_JOB = "<JOB_NAME>" # without '/job' 
TOKEN_NAME = "<API_TOKEN>"
# Example Parameter
PARAMETERS = {'DISPLAY': 'something new', 'SLEEP_SECONDS': '30'}

class DevOpsJenkins:
    def __init__(self):
        self.jenkins_server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        print ("Jenkins Version: {}".format(version))
        print ("Jenkins User: {}".format(user['id']))

    def build_job(self):
        next_build_number = self.jenkins_server.get_job_info(NAME_OF_JOB)['nextBuildNumber']
        self.jenkins_server.build_job(NAME_OF_JOB, parameters=PARAMETERS, token=TOKEN_NAME)
        time.sleep(10)
        # build_info = self.jenkins_server.get_build_info(name, next_build_number)
        # return build_info
        # return build_info['queueId']
        return next_build_number
    
    def poll_status(self, next_build_number):
        job_url_shown = False
        while True:           
            time.sleep(15)
            build_info = self.jenkins_server.get_build_info(NAME_OF_JOB, next_build_number)
            # print(build_info)
            if build_info["result"] is None:
                if not job_url_shown:
                    print(f"\nRunning: {build_info['url']}\n")
                    job_url_shown = True
                print(".", end="", flush=True)
            else:
                if build_info['result'] == 'SUCCESS':
                    print('Finished Successfully.')
                    return 0
                else:
                    print('FAILED!!')
                    return 1


if __name__ == "__main__":
    jenkins_obj = DevOpsJenkins()
    next_build_number = jenkins_obj.build_job()
    exit_code = jenkins_obj.poll_status(next_build_number)
    sys.exit(exit_code)
