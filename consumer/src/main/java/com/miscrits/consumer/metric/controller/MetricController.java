package com.miscrits.consumer.metric.controller;

import com.miscrits.consumer.metric.service.MetricService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
public class MetricController {

    private final MetricService metricServiceImpl;

    @GetMapping("/find/metric")

    @GetMapping("/target/metric")

    @GetMapping("/capture/metric")

}
