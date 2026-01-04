package com.miscrits.consumer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class MiscritInfo {

    private String miscritName;
    private boolean isHighGradeOrRare;

    // This is the percentage of initial capture rate represented by an integer
    private Integer initialCaptureRate;

}
