import json
import os

from copy import deepcopy
from slack_sdk import WebClient


with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
    K8S_NAMESPACE = f.read().strip()
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL = {
    'shopify': '#production-alerts',
    'shopify-staging': '#staging-alerts'
}.get(K8S_NAMESPACE)
NOTIFY_CHANNEL = True


class Slack:
    slack_client = WebClient(token=SLACK_API_TOKEN)

    def send_alert(self, msg: dict):
        bdy = deepcopy(msg['bdy'])
        channel = bdy.get('channel', SLACK_CHANNEL)
        channel = channel if channel.startswith('#') else '#' + channel
        notify_str = '<!here>' if bdy.get('notify_channel', NOTIFY_CHANNEL) else ''
        for item_to_remove in ['channel', 'notify_channel']:
            if item_to_remove in bdy:
                del bdy[item_to_remove]
        txt = f"{notify_str} Skafos `{K8S_NAMESPACE}` Alert From --> `{msg['frm']}` "
        txt += f"```{json.dumps(bdy)}```"
        if channel:
            response = self.slack_client.chat_postMessage(channel=channel, text=txt)
