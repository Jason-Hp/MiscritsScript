package com.miscrits.consumer.consumer;

import org.apache.kafka.clients.consumer.ConsumerRecord;

public interface Consumer {

    public void consume(ConsumerRecord<String, String> record);

}
