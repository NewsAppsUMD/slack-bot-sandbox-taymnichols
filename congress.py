import os
import json
import requests
from slack import WebClient
from slack.errors import SlackApiError

congress_key = os.environ.get('CONGRESS_API_KEY')
slack_token = os.environ.get('SLACK_API_TOKEN')

url = "https://api.congress.gov/v3/committee-report/118?format=json"

r=requests.get(url, headers={'x-api-key': congress_key})

reports = r.json()['reports']
first_report = reports[0]

msg = f"The latest committee report is {first_report['citation']}, which was issued on {first_report['updateDate']}. The URL is {first_report['url']}"
client = WebClient(token=slack_token)
try:
    response = client.chat_postMessage(
        channel="slack-bots",
        text=msg,
        unfurl_links=True, 
        unfurl_media=True
    )
    print("success!")
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")