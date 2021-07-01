import asyncio
import traceback

from lib.slack import Slack
from smslib.utils import BaseProcessor
from smslib.utils import Logger


MIN_MESSAGE_CHECK_DELAY = 0   # 0 milliseconds
MAX_MESSAGE_CHECK_DELAY = 1   # 1000 milliseconds
MESSAGE_CHECK_DELAY = 0.1     # 100 milliseconds

class Processor(BaseProcessor):
    async def init(self, messenger, service_name):
        self.messenger = messenger
        self.service_name = f'{service_name}:/'
        self.slack = Slack()
        asyncio.create_task(self.check_for_tasks())

    async def check_for_tasks(self):
        """Check for queued messages/tasks to the service."""
        while True:
            msg = await self.messenger.get_queue_message(self.service_name)
            if self.valid_msg(msg):
                await self.process(msg)
                await self.messenger.mark_queue_message(msg, True, 'Message handled')
                self.message_check_delay = MIN_MESSAGE_CHECK_DELAY
            else:
                self.message_check_delay = min(max(self.message_check_delay + MESSAGE_CHECK_DELAY, MIN_MESSAGE_CHECK_DELAY), MAX_MESSAGE_CHECK_DELAY)
            await asyncio.sleep(self.message_check_delay)

    async def process(self, msg):
        try:
            logger = Logger(self.messenger, msg)
            if msg['typ'] == 'slack_alerts.send':
                await self.send(msg, logger)
            else:
                await logger.log(f'Invalid message type: {msg["typ"]}')
        except Exception as e:
            await logger.error(traceback.format_exc())

    async def send(self, msg, logger):
        await logger.log(msg)
        self.slack.send_alert(msg)
