package com.miscrits.consumer.metric.response;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class CapturedMiscritsResponse {

    private List<String> capturedMiscrits;

}
