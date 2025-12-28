package com.miscrits.consumer.mail.impl;

import com.miscrits.consumer.mail.MailService;
import com.miscrits.consumer.pojo.AlertEmail;
import lombok.AllArgsConstructor;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class GmailServiceImpl implements MailService {

    private final JavaMailSender javaMailSender;

    public void mail(AlertEmail alertEmail) {
        SimpleMailMessage simpleMailMessage = new SimpleMailMessage();
        simpleMailMessage.setFrom(alertEmail.getRecipient());
        simpleMailMessage.setTo(alertEmail.getRecipient());
        simpleMailMessage.setText(alertEmail.getBody());
        simpleMailMessage.setSubject(alertEmail.getSubject());

        try {
            javaMailSender.send(simpleMailMessage);
        } catch (Exception e) {
            throw new RuntimeException("Something went wrong when gmailing to " + alertEmail.getRecipient());
        }
    }

}
