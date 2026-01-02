package com.miscrits.consumer.consumer.impl;

import com.miscrits.consumer.consumer.Consumer;
import lombok.AllArgsConstructor;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class FindConsumerImpl implements Consumer {

    private final com.miscrits.consumer.service.Service findServiceImpl;

    @KafkaListener(topics = "find-action", groupId = "miscrit-consumer")
    public void consume(ConsumerRecord<String, String> record) {
        String key = record.key();
        String value = record.value();
        findServiceImpl.operate(value);
    }

}
