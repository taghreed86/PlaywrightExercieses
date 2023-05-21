from urllib import request
import json
import sys


def main(argv):
    result = argv[0]
    branch = argv[1]
    url = argv[2]
    tests = argv[3]

    hook = "https://hooks.slack.com/services/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"
    env = "Enterprise"
    message = f"{result}: {tests} Test on\n{env}: `{branch}`\n<{url}|View In Github Actions>"

    if result == "SUCCESS":
        color = "good"
    elif result == "FAILURE":
        color = "danger"

    post = {
      "type": "mrkdwn",
      "attachments": [
        {
          "fields": [
            {"value": message, "short": "false"}
          ],
          "color": color,
          "ts":  "timestamp"
        }
      ]
    }

    try:
        json_data = json.dumps(post)
        print(json_data)
        req = request.Request(hook,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))


if __name__ == "__main__":
    main(sys.argv[1:])