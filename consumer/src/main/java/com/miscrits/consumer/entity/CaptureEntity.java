package com.miscrits.consumer.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "capture")
public class CaptureEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "is_captured")
    private boolean isCaptured;

    @Column(name = "miscrit_name")
    private String miscritName;

    @Column(name = "action_id", unique = true)
    @OneToOne(targetEntity = FindEntity.class)
    private Long actionId;

}
