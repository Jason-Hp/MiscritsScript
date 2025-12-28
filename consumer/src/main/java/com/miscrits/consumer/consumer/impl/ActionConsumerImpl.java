package com.miscrits.consumer.consumer.impl;

import com.miscrits.consumer.consumer.Consumer;
import com.miscrits.consumer.service.FacadeService;
import lombok.AllArgsConstructor;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class ActionConsumerImpl implements Consumer {

    private final FacadeService facadeService;

    @KafkaListener(topics = "action", groupId = "action-consumer")
    public void consume(ConsumerRecord<String, String> record) {
        String key = record.key();
        String value = record.value();
        facadeService.call(key, value);
    }

}
