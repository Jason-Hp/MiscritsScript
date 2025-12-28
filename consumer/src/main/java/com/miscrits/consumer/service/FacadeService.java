package com.miscrits.consumer.service;

import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class FacadeService {
    //todo in config
    Map<String, com.miscrits.consumer.service.Service> serviceMap;

    public void call(String key, String value) {
        com.miscrits.consumer.service.Service service = serviceMap.get(key);
        if (service == null) {
            // todo alert :)
            throw new RuntimeException("No service found for key: " + key);
        }
        service.operate(value);
    }
}
