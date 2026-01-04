package com.miscrits.consumer.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@Data
@Table(name = "find")
public class FindEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    // This field is false only if there is a CONSECUTIVE_FAILURES, and is not the same as the field in Action POJO
    @Column(name = "is_successful")
    private boolean isSuccessful;

    @Column(name = "action_id")
    private Long actionId;

}
