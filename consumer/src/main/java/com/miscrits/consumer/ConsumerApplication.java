package com.miscrits.consumer;

import com.miscrits.consumer.alert.Alert;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConsumerApplication {
	public static void main(String[] args) {

        // TODO args here to set up MISCRIT NAME
        Alert errorAlertImpl;

        try {
            SpringApplication.run(ConsumerApplication.class, args);
        } catch (Exception e) {

        }
	}

}
