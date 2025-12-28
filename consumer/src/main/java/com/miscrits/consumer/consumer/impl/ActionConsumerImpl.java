package com.miscrits.consumer.consumer.impl;

import com.miscrits.consumer.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class ActionConsumerImpl implements Consumer {

    // no need for more arguments like group id, as only 1 instance of Consumer is running
    @KafkaListener(topics = "{action}")
    public void consume(ConsumerRecord<String, String> record) {
        String key = record.key();
        String value = record.value();
    }

}
