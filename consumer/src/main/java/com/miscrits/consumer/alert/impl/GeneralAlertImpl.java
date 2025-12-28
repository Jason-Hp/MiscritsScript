package com.miscrits.consumer.alert.impl;

import com.miscrits.consumer.alert.Alert;
import org.springframework.stereotype.Service;

@Service
public class GeneralAlertImpl implements Alert {

    private final String GENERAL_SUBJECT = "General - ";

    @Override
    public String type() {
        return "general";
    }

    @Override
    public void alert() {

    }

    @Override
    public String formatSubject(String title) {
        return GENERAL_SUBJECT + title;
    }

    @Override
    public String formatMessage(String message) {
        return message;
    }
}
