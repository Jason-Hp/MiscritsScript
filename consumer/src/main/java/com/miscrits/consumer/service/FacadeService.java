package com.miscrits.consumer.service;

import com.miscrits.consumer.alert.Alert;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Map;

import static com.miscrits.consumer.alert.AlertInformation.NO_SERVICE_FOUND;

@Service
@AllArgsConstructor
public class FacadeService {

    private final Map<String, com.miscrits.consumer.service.Service> serviceMap;

    private final Alert errorAlertImpl;

    public void call(String key, String value) {
        com.miscrits.consumer.service.Service service = serviceMap.get(key);
        if (service == null) {
            errorAlertImpl.alert(NO_SERVICE_FOUND);
            throw new RuntimeException("No service found for key: " + key);
        }
        service.operate(value);
    }
}
