package com.miscrits.consumer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class MiscritInfo {

    private String miscritName;
    private boolean isHighGradeOrRare;
    private Integer initialCaptureRate;

}
