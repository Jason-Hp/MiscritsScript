package com.miscrits.consumer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class AlertEmail {

    private String subject;
    private String body;
    private String recipient;

}
