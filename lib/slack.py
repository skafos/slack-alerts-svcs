import json
import os
from slack_sdk import WebClient


with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
    K8S_NAMESPACE = f.read().strip()
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL = {
    'shopify': '#production-alerts',
    'shopify-staging': '#staging-alerts'
}.get(K8S_NAMESPACE)


class Slack:
    slack_client = WebClient(token=SLACK_API_TOKEN)

    def send_alert(self, msg: dict):
        txt = f"<!here> Skafos `{K8S_NAMESPACE}` Alert From --> `{msg['frm']}` "
        txt += f"```{json.dumps(msg['bdy'])}```"
        if SLACK_CHANNEL:
            response = self.slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=txt)
