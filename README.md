# MiscritsScript
A simple script leveraging python and pyautogui to automate the process of finding and/or training your miscrits

## Kafka producer helper

The repository now includes a lightweight Kafka producer utility (`kafka_producer.py`) that mirrors the payloads
expected by the Spring Boot consumer service.

1. Install the dependency: `pip install kafka-python`.
2. Configure the connection (optional):
   - Pass custom values to `KafkaSettings(bootstrap_servers=..., client_id=..., find_action_topic=..., miscrit_info_topic=...)`
   - Otherwise the defaults of `localhost:9092`, `miscrits-script`, `find-action`, and `miscrit-info` are used.
3. Publish events using the helper classes:

```python
from kafka_producer import Action, MiscritInfo, MiscritsKafkaProducer

producer = MiscritsKafkaProducer()

# Send a find action (Kafka key controls which Spring service handles it)
producer.send_action(Action(id=123, is_successful=True, description="locust map", name="find"), key="find")

# Send information about the miscrit encountered
producer.send_miscrit_info(MiscritInfo(miscrit_name="Papa", is_high_grade_or_rare=True, initial_capture_rate=72))

producer.flush()
```

You can also call `publish_kafka_examples()` inside `miscritScript.py` for a runnable example.
