package com.miscrits.consumer.alert.impl;

import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import com.miscrits.consumer.mail.MailService;
import com.miscrits.consumer.pojo.AlertEmail;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ErrorAlertImpl implements Alert {

    private final String ERROR_SUBJECT = "ERROR - ";

    // Mail to self
    @Value("${spring.mail.username}")
    private final String RECIPIENT;

    private final MailService mailService;

    @Override
    public String type() {
        return "error";
    }

    @Override
    public void alert(AlertInformation alertInformation) {
        String title = alertInformation.title;
        String message = alertInformation.body;

        String subject = formatSubject(title);
        String messageBody = formatMessage(message);
        AlertEmail alertEmail = new AlertEmail(subject, messageBody, RECIPIENT);

        mailService.mail(alertEmail);
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
