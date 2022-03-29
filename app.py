import asyncio

from lib.processor import Processor
from smslib.utils import BaseService


class SlackAlertsService(BaseService):
    processor = Processor()     # message processor


if __name__ == '__main__':
    slack_alerts_service = SlackAlertsService()
    asyncio.run(slack_alerts_service.main())
