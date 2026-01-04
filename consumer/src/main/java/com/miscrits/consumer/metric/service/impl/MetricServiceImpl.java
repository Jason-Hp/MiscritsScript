package com.miscrits.consumer.metric.service.impl;

import com.miscrits.consumer.metric.response.*;
import com.miscrits.consumer.metric.service.MetricService;
import com.miscrits.consumer.repository.CaptureRepository;
import com.miscrits.consumer.repository.FindRepository;
import com.miscrits.consumer.repository.MiscritRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class MetricServiceImpl implements MetricService {

    //TODO May need to refactor using Builder pattern instead of using constructors in case of new additions to classes

    private final FindRepository findRepository;

    private final MiscritRepository miscritRepository;

    private final CaptureRepository captureRepository;

    public FindMetricResponse getFindSuccessRateMetric() {
        double successRate = (double) findRepository.countByIsSuccessfulTrue() / findRepository.count();
        String successRateString = Double.toString(successRate) + "%";
        return new FindMetricResponse(successRateString);
    }

    public TargetMiscritMetricResponse getTargetMiscritEncounteredMetric(String targetMiscrit) {
        double targetMiscritEncounteredRate = (double) miscritRepository.countByNameAndTargetMiscrit(targetMiscrit, targetMiscrit) / miscritRepository.countByTargetMiscrit(targetMiscrit);
        return new TargetMiscritMetricResponse(targetMiscritEncounteredRate + "%", targetMiscrit);
    }

    public HighGradeOrRareMetricResponse getNumberOfHighGradeOrRareMetric() {
        long count = miscritRepository.countByHighGradeOrRareTrue();
        return new HighGradeOrRareMetricResponse(count);
    }

    public CaptureRateMetricResponse getCaptureSuccessRateMetric() {
        double captureRate = (double) captureRepository.countByCapturedTrue() / captureRepository.count();
        return new CaptureRateMetricResponse(captureRate + "%");
    }

    public CapturedMiscritsResponse getCapturedMiscrits() {
        List<String> capturedMiscrits = captureRepository.findAllCapturedMiscritNames();
        return new CapturedMiscritsResponse(capturedMiscrits);
    }

}
