import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from aiohttp import ClientResponse
from aiokafka.structs import ConsumerRecord

from subscriber import Subscriber

@pytest.fixture
def subscriber(mock_logger):
    subscriber = Subscriber(mock_logger)
    yield subscriber
    subscriber.shutdown()

@pytest.mark.asyncio
async def test_send_one(subscriber):
    
    # Mock the producer so it doesn't actually try to send messages
    subscriber.producer = AsyncMock()

    # Run the send_one method
    await subscriber.send_one('test_topic', 'test_message')

    # Assert that the producer's send_and_wait method was called with the correct arguments
    subscriber.producer.send_and_wait.assert_called_once_with('test_topic', 'test_message')

@pytest.mark.asyncio
async def test_consume(subscriber):
    
    # Mock the subscribe method so it doesn't actually try to make HTTP requests
    subscriber.subscribe = AsyncMock()

    # Run the setup method
    await subscriber.setup()

    # Stop the real consumer and producer
    await subscriber.consumer.stop()
    await subscriber.producer.stop()

    # Create a test message
    test_message = ConsumerRecord(
        topic="subscription_requests",
        partition=0,
        offset=0,
        key=None,
        value={"external_api_url": "http://test.com", "json_data": {}},
        timestamp=None,
        timestamp_type=None,
        headers=[],
        checksum=None,
        serialized_key_size=0,
        serialized_value_size=0
    )

    # Mock the AIOKafkaConsumer to simulate receiving the test message
    subscriber.consumer = AsyncMock()
    subscriber.consumer.__aiter__.return_value = iter([test_message])

    # Run the consume method
    await subscriber.consume()

    # Assert that the subscribe method was called with the test message
    subscriber.subscribe.assert_called_once_with(test_message)

@pytest.mark.asyncio
async def test_subscribe(subscriber):
    subscriber.send_one = AsyncMock()
    subscriber.callback = AsyncMock()

    # Create a test payload
    payload = {"external_api_url": "http://test.com", "json_data": {}}

    # Mock the aiohttp.ClientSession to simulate making an HTTP request
    with patch('aiohttp.ClientSession.post') as mock_post:
        # Create a mock response with a 200 status
        mock_response = MagicMock(spec=ClientResponse)
        mock_response.status = 200

        # Create a mock context manager to return the mock response
        mock_context_manager = MagicMock()
        mock_context_manager.__aenter__.return_value = mock_response
        mock_context_manager.__aexit__.return_value = None

        # Set up the mock post method to return the mock context manager
        mock_post.return_value = mock_context_manager

        # Run the subscribe method
        await subscriber.subscribe(payload)

    # Assert that the send_one method was called with the correct arguments
    subscriber.send_one.assert_called_once_with("successful_subscription_requests", payload)