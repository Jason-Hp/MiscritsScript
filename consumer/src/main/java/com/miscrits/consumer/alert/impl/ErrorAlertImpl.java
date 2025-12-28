package com.miscrits.consumer.alert.impl;

import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.pojo.AlertEmail;
import org.springframework.stereotype.Service;

@Service
public class ErrorAlertImpl implements Alert {

    //TODO try to make red?
    private final String ERROR_SUBJECT = "ERROR - ";
    //todo put email receipiant in properties

    @Override
    public String type() {
        return "error";
    }

    @Override
    public void alert(String message, String title) {
        String subject = formatSubject(title);
        String messageBody = formatMessage(message);
        AlertEmail alertEmail = new AlertEmail(subject, messageBody);
        // mail this
    }

    @Override
    public String formatSubject(String title) {
        return ERROR_SUBJECT + title;
    }

    @Override
    public String formatMessage(String message) {
        return message;
    }
}
