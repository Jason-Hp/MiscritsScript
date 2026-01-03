package com.miscrits.consumer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Action {

    // This id is not a primary key or a typical id, it is to group several actions that belong to the
    // same miscrit find-battle-capture process together
    private Long id;

    private Boolean isSuccessful;
    private String description;
    private String name;
}
