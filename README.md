# Slack Alerts Service

Hydra-Py microservice that wraps the Python `slack-sdk` library. The service is intended to be used within a larger microservice architecture. It also requires a slack `SLACK_API_TOKEN`.


## Usage
To trigger an alert message in either `#production-alerts` or `#staging-alerts` channels, send or queue a message to the service like below:

```
{
  "frm": "some-v1-svcs:/",
  "to": "slack-alerts-svcs:/",
  "mid": "951bdaf6-6199-419a-bba8-02feb993c63e",
  "ts": "2021-01-21T19:40:38.333Z",
  "ver": "UMF/1.4.6",
  "typ": "slack_alerts.send",
  "bdy": {
   "testing": "testing"
  }
}
```

The service will authenticate the request using the API token and send the `bdy` of the message to the slack channel based on the k8s namespace (in order to know the environment).

Alternatively, if you wish to send to a different channel, indicate the channel in the body of the message, like so:

```
{
  "frm": "some-v1-svcs:/",
  "to": "slack-alerts-svcs:/",
  "mid": "951bdaf6-6199-419a-bba8-02feb993c63e",
  "ts": "2021-01-21T19:40:38.333Z",
  "ver": "UMF/1.4.6",
  "typ": "slack_alerts.send",
  "bdy": {
   "testing": "testing",
   "channel": "general"
  }
}
```