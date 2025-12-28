package com.miscrits.consumer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Action {
    private Long id;
    private Boolean isSuccessful;
    private String description;
    private String name;
}
