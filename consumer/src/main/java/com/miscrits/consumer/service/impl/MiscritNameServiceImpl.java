package com.miscrits.consumer.service.impl;

import com.google.gson.Gson;
import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import com.miscrits.consumer.pojo.MiscritInfo;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Map;

import static com.miscrits.consumer.alert.AlertInformation.GENERAL_MESSAGE;

@Service
@AllArgsConstructor
public class MiscritNameServiceImpl implements com.miscrits.consumer.service.Service {

    private final Map<String, Alert> alertMap;

    //TODO wire in from args
    private final String targetMiscrit;

    private final Gson gson;

    @Override
    public String key() {
        return "name";
    }

    @Override
    public void operate(String value) {

        MiscritInfo miscritInfo = gson.fromJson(value,MiscritInfo.class);

        // Found target miscrit
        if (miscritInfo.getMiscritName().equalsIgnoreCase(targetMiscrit)) {
            AlertInformation generalMessage = GENERAL_MESSAGE;
            generalMessage.setTitle("FOUND " + miscritInfo.getMiscritName());
            generalMessage.setBody("FOUND " + miscritInfo.getMiscritName());

            updateMiscritMetrics(true, miscritInfo.getMiscritName());

        } else {
            updateMiscritMetrics(false, miscritInfo.getMiscritName());
        }

    }

    private void updateMiscritMetrics(boolean isTargetFound, String miscritFound) {
        //TODO IMPLEMENT
    }
}
