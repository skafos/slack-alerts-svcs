import traceback

from lib.slack import Slack
from smslib.utils import BaseProcessor
from smslib.utils import Logger


class Processor(BaseProcessor):
    async def init(self, messenger, service_name):
        self.messenger = messenger
        self.service_name = f'{service_name}:/'
        self.slack = Slack()
        self.register_routes({
            'slack_alerts.send': self.send
        }, roles=['admin'])
        await self.check_for_tasks()

    async def process(self, msg):
        try:
            logger = Logger(self.messenger, msg)
            await self.execute(msg, logger)
        except Exception:
            await logger.error(traceback.format_exc())

    async def send(self, msg, logger):
        await logger.log(msg)
        self.slack.send_alert(msg)
