import asyncio

from hydrapy import HydraPy
from lib.processor import Processor


class SlackAlertsService:
    hydra = None                # hydra instance
    si = None                   # service info
    processor = Processor()     # message processor

    async def main(self):
        service_version = open('VERSION').read().rstrip()
        self.hydra = HydraPy(
            config_path='./config/config.json',
            version=service_version,
            message_handler=self.processor.handle_message,
            queue_handler=None
        )
        self.si = await self.hydra.init()
        await self.processor.init(self.hydra, self.si['serviceName'])
        start_message = f"{self.si['serviceName']}({self.si['instanceID']})(v{self.si['serviceVersion']}) running at {self.si['serviceIP']}"
        print(start_message, flush=True)
        await self.hydra.log(HydraPy.INFO, {}, start_message)
        await self.hydra.run()


slack_alerts_service = SlackAlertsService()
asyncio.run(slack_alerts_service.main())
