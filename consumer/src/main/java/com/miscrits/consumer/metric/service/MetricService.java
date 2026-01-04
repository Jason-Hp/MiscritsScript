package com.miscrits.consumer.metric.service;

import com.miscrits.consumer.metric.response.*;

public interface MetricService {

     FindMetricResponse getFindSuccessRateMetric();

     TargetMiscritMetricResponse getTargetMiscritEncounteredMetric(String targetMiscrit);

     HighGradeOrRareMetricResponse getNumberOfHighGradeOrRareMetric();

     CaptureRateMetricResponse getCaptureSuccessRateMetric();

     CapturedMiscritsResponse getCapturedMiscrits();

}
