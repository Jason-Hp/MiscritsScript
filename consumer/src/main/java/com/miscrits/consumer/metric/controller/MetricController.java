package com.miscrits.consumer.metric.controller;

import com.miscrits.consumer.metric.response.*;
import com.miscrits.consumer.metric.service.MetricService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
@RequestMapping("/metric")
public class MetricController {

    private final MetricService metricServiceImpl;

    @GetMapping("/find")
    public FindMetricResponse getFindMetricResponse() {
        return metricServiceImpl.getFindSuccessRateMetric();
    }

    @GetMapping("/miscrit/target/{targetMiscrit}")
    public TargetMiscritMetricResponse getTargetMiscritEncounteredMetric(@PathVariable String targetMiscrit) {
        return metricServiceImpl.getTargetMiscritEncounteredMetric(targetMiscrit);
    }

    @GetMapping("/miscrit/high-grade-or-rare")
    public HighGradeOrRareMetricResponse getNumberOfHighGradeOrRareMetric() {
        return metricServiceImpl.getNumberOfHighGradeOrRareMetric();
    }

    @GetMapping("/capture/rate")
    public CaptureRateMetricResponse getCaptureSuccessRateMetric() {
        return metricServiceImpl.getCaptureSuccessRateMetric();
    }

    @GetMapping("/capture/miscrits")
    public CapturedMiscritsResponse getCapturedMiscrits() {
        return metricServiceImpl.getCapturedMiscrits();
    }



}
