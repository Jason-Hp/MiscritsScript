package com.miscrits.consumer.service.impl;

import com.google.gson.Gson;
import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import com.miscrits.consumer.entity.CaptureEntity;
import com.miscrits.consumer.pojo.Action;
import com.miscrits.consumer.repository.CaptureRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@AllArgsConstructor
public class CaptureServiceImpl implements com.miscrits.consumer.service.Service {

    /**
     * This service exists because I am unable to implement an
     * unsuccessful capture check for
     * the Python Miscrit Automation script
     * <p>
     * Also, this is for general fodder/high grade miscrits capture, rather
     * than the target miscrit capture as they need more delicate handling, which
     * currently only the actual user can perform manually
     */

    private final Gson gson;

    private final Alert errorAlertImpl;

    private final CaptureRepository captureRepository;

    private Action prevCaptureAction = null;

    @Override
    public String key() {
        return "capture";
    }

    @Override
    public void operate(String value) {
        Action captureAction = gson.fromJson(value, Action.class);

        if (prevCaptureAction == null) {
            prevCaptureAction = captureAction;

            // Assume first capture action results in successful capture
            upsertCaptureInfo(true, captureAction);
            return;
        }

        if (prevCaptureAction.getId().equals(captureAction.getId())) {
            upsertCaptureInfo(false, captureAction);
            errorAlertImpl.alert(AlertInformation.CONSECUTIVE_CAPTURES);
        } else {
            upsertCaptureInfo(true, captureAction);
            prevCaptureAction = captureAction;
        }
    }

    private void upsertCaptureInfo(boolean isCaptured, Action captureAction) {

        CaptureEntity captureEntity = Optional.ofNullable(captureRepository.getByActionId(captureAction.getId())).orElse(
                CaptureEntity.builder()
                        .isCaptured(isCaptured)
                        .miscritName(captureAction.getDescription())
                        .actionId(captureAction.getId())
                        .build()
        );

        // Set again if managed to retrieve from DB
        captureEntity.setCaptured((isCaptured));

        captureRepository.save(captureEntity);
    }
}
