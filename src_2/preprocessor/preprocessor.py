import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import aiohttp

class Preprocessor:
  
  def __init__(self, logger):
    self.logger = logger
    self.consumer = None
    self.producer = None

  async def setup(self):
    self.consumer = AIOKafkaConsumer(
        'triggered_subscriptions',
        bootstrap_servers='localhost:9092',
        group_id="my-group")
    self.producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')

    await self.consumer.start()
    await self.producer.start()

  def run(self):
    """Start an asyncio event loop and run setup and consume until completes"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.setup())
    loop.run_until_complete(self.consume())
    
  async def shutdown(self):
    await self.consumer.stop()
    await self.producer.stop()

  async def consume(self):
    """An asychronous generator that keeps yielding messages from the kafka topic until the consumer is stopped. The finally block is there to make sure that the consumer and producer are cleanly stopped even in the case of errors"""
    try:
        # Consume messages
        async for msg in self.consumer:
            self.logger.debug("consumed: ", msg)
            await self._handle_consumed(msg)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await self.consumer.stop()
        await self.producer.stop()

  async def send_one(self, topic, msg):
    # Produce message
    await self.producer.send_and_wait(topic, msg)
    
  async def _handle_consumed(self, payload):
    try:
      # process the message then send it to the next topic
      x = 2
    except Exception as error:
      payload["error"] = str(error)
      await self.send_one("error", payload)
