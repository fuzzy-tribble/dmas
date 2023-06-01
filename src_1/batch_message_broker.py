"""
Messenger for mas


"""
from typing import List
import random
import string
import json
import psycopg2
from kafka import KafkaAdminClient, NewTopic

class Messenger:
    """Messenger for mas"""
    def __init__(self, endpoint, users: List[object]):
        self.endpoint = endpoint
        self.manager_usernames = manager_usernames
        self.agent_username = agent_username
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=[self.endpoint],
            client_id='test-admin'
        )

        # Generate API keys for managers
        for manager_username in self.manager_usernames:
            api_key, api_secret = self._generate_api_key()
            self._save_api_key_to_file(manager_username, api_key, api_secret)

        # Generate API key for agent
        api_key, api_secret = self._generate_api_key()
        self._save_api_key_to_db(self.agent_username, api_key, api_secret)

    def _generate_api_key(self):
        # Generate random API key and secret
        api_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        api_secret = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        return api_key, api_secret

    def _save_api_key_to_file(self, username, api_key, api_secret):
        # Save API key and secret to file
        with open(f"{username}.json", "w") as f:
            json.dump({"api_key": api_key, "api_secret": api_secret}, f)

    def _save_api_key_to_db(self, username, api_key, api_secret):
        # Save API key and secret to database
        conn = psycopg2.connect(database="mydb", user="myuser", password="mypassword", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO api_keys (username, api_key, api_secret) VALUES (%s, %s, %s)", (username, api_key, api_secret))
        conn.commit()
        cursor.close()
        conn.close()

    def create_topic(self, topic_name):
        # Create new topic with replication factor of 3 and 3 partitions
        topic = NewTopic(name=topic_name, num_partitions=3, replication_factor=3)
        futures = self.admin_client.create_topics([topic])
        for _, future in futures.items():
            try:
                future.result()
                print(f"Topic '{topic_name}' created")
            except Exception as e:
                print(f"Failed to create topic '{topic_name}': {e}")

    def send_message(self, topic, message, sender_id):
        retries = 0
        headers = [("sender", sender_id)]
        while retries < self.max_retries:
            try:
                self.producer.send(topic, value=message, headers=headers)
                break
            except KafkaError as ke:
                print(f"Failed to send message to topic '{topic}': {ke}")
                retries += 1
        if retries >= self.max_retries:
            raise KafkaError(f"Failed to send message to topic '{topic}' after {self.max_retries} retries")

    def consume_messages(self, topic, group_id):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[self.endpoint],
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=self.api_key,
            sasl_plain_password=self.api_secret,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: x.decode('utf-8')
        )
        for message in consumer:
            yield message.value