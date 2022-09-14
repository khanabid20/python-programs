#!/usr/bin/env python3
import argparse
import sys
import time, datetime

import requests

JENKINS_API_TOKEN = "<JENKINS_API_TOKEN>"
JENKINS_USERNAME = "<USERNAME>"
JENKINS_PASSWORD = JENKINS_API_TOKEN
JENKINS_JOB_URL = f'https://{JENKINS_USERNAME}:{JENKINS_PASSWORD}@<SERVER_URL>/job/<JOB_NAME>'    # with '/job' if it's inside folders

api_req = requests.Session()
api_req.headers.update(
    {
        "Authorization": "Basic BASIC_USER_AUTH",
        "Content-Type": "application/x-www-form-urlencoded",
    }
)


def main():
    parser = argparse.ArgumentParser(description="Run a GitLab MR job on Jenkins and poll for the result.")
    parser.add_argument("--display_msg", required=True, type=str)
    parser.add_argument("--sleep_seconds", required=True, type=str)
    args = parser.parse_args(sys.argv[1:])

    queue_id = schedule_build(args)
    exit_code = poll_build(queue_id)
    print(datetime.datetime.now())
    sys.exit(exit_code)


def schedule_build(args: argparse.Namespace) -> int:
    response = api_req.post(
        f"{JENKINS_JOB_URL}/buildWithParameters?token={JENKINS_API_TOKEN}",
        data={
            "DISPLAY": args.display_msg,
            "SLEEP_SECONDS": args.sleep_seconds,
        },
    )
    response.raise_for_status()
    location_header_value = response.headers["Location"]
    # Example location header: "https://jenkins.example.org/queue/item/123/"
    return int(location_header_value.rstrip("/").split("/")[-1])


def poll_build(queue_id: int) -> int:
    job_url_shown = False

    for _ in range(300):
        time.sleep(15)
        response = api_req.get(f"{JENKINS_JOB_URL}/api/json?tree=builds[result,queueId,url]")
        response.raise_for_status()

        for build in response.json()["builds"]:
            if build["queueId"] != queue_id:
                continue
            elif build["result"] is None:
                if not job_url_shown:
                    # Scheduled job first appeared; show URL.
                    print(f"\nRunning: {build['url']}\n")
                    job_url_shown = True
                print(".", end="", flush=True)
            else:
                if build["result"] == "SUCCESS":
                    print(build['result'])
                    return 0
                else:
                    print(build['result'])
                    return 1


if __name__ == "__main__":
    print(datetime.datetime.now())
    main()

'''
refs:
- https://devops.stackexchange.com/a/16073/8560
'''
