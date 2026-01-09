package com.miscrits.consumer.consumer.impl;

import com.miscrits.consumer.consumer.Consumer;
import lombok.AllArgsConstructor;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
@AllArgsConstructor
public class FindConsumerImpl implements Consumer {

    private final Map<String, com.miscrits.consumer.service.Service> serviceMap;

    @KafkaListener(topics = "action", groupId = "miscrit-consumer")
    public void consume(ConsumerRecord<String, String> record) {
        String key = record.key();
        String value = record.value();

        com.miscrits.consumer.service.Service service = serviceMap.get(key);
        service.operate(value);
    }

}
