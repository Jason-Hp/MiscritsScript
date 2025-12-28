package com.miscrits.consumer.configuration;

import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.service.Service;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Configuration
public class Config {

    @Bean
    public Map<String, Service> serviceMap(List<Service> services) {
        return services.stream().collect(Collectors.toMap(Service::key, service -> service));
    }

    @Bean
    public Map<String, Alert> alertMap(List<Alert> alerts) {
        return alerts.stream().collect(Collectors.toMap(Alert::type, alert -> alert));
    }

}
