package com.miscrits.consumer.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@Data
@Table(name = "miscrits")
public class MiscritEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    private String name;

    @Column(name = "is_high_grade_or_rare")
    private boolean isHighGradeOrRare;

    @Column(name = "initial_capture_rate")
    private Integer initialCaptureRate;

    @Column(name = "target_miscrit")
    private String targetMiscrit;

}
