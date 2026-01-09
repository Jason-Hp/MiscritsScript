package com.miscrits.consumer.service.impl;

import com.google.gson.Gson;
import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import com.miscrits.consumer.entity.MiscritEntity;
import com.miscrits.consumer.pojo.MiscritInfo;
import com.miscrits.consumer.repository.MiscritRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Map;

import static com.miscrits.consumer.alert.AlertInformation.GENERAL_MESSAGE;

@Service
@RequiredArgsConstructor
public class MiscritNameServiceImpl implements com.miscrits.consumer.service.Service {

    private final Map<String, Alert> alertMap;

    @Value("${miscrits.target-miscrit}")
    private String targetMiscrit;

    private final Gson gson;

    private final MiscritRepository miscritRepository;

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

            alertMap.get("general").alert(generalMessage);

        }

        MiscritEntity miscritEntity = new MiscritEntity();
        miscritEntity.setName(miscritInfo.getMiscritName());
        miscritEntity.setTargetMiscrit(targetMiscrit);
        miscritEntity.setHighGradeOrRare(miscritInfo.isHighGradeOrRare());
        miscritEntity.setInitialCaptureRate(miscritInfo.getInitialCaptureRate());

        miscritRepository.save(miscritEntity);
    }

}
