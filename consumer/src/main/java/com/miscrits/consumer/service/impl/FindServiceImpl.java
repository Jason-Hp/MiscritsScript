package com.miscrits.consumer.service.impl;

import com.google.gson.Gson;
import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import com.miscrits.consumer.pojo.Action;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayDeque;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.atomic.AtomicBoolean;

import static com.miscrits.consumer.alert.AlertInformation.CONSECUTIVE_FAILURES;
import static com.miscrits.consumer.alert.AlertInformation.GENERAL_MESSAGE;

@Service
@AllArgsConstructor
public class FindServiceImpl implements com.miscrits.consumer.service.Service {

    // item drop is 0.05, 5 item drops in a row is (0.05)^5 =  0.00000003125
    private final int SIZE_OF_QUEUE = 5;

    private final Queue<Action> previousFinds = new ArrayDeque<>(SIZE_OF_QUEUE);

    private final Map<String, Alert> alertMap;

    private final Gson gson = new Gson();

    @Override
    public String key() {
        return "find";
    }

    @Override
    public void operate(String value) {
        Action findAction = gson.fromJson(value, Action.class);

        // look through past SIZE_OF_QUEUE finds
        AtomicBoolean failedAll = new AtomicBoolean(true);

        if (!findAction.getIsSuccessful()) {
            previousFinds.forEach(previousFind -> {
                if (previousFind.getIsSuccessful()) {
                    failedAll.set(false);
                }
            });
        }
        if (failedAll.get()) {
            Alert alert = alertMap.get("error");
            if (alert == null) {
                throw new RuntimeException("Error alert cannot be found?!");
            }
            alert.alert(CONSECUTIVE_FAILURES);
            return;
        }
        previousFinds.offer(findAction);

        Alert generalAlert = alertMap.get("general");
        AlertInformation generalMessage = GENERAL_MESSAGE;
        generalMessage.setTitle(findAction.getName());
        generalMessage.setBody(findAction.getDescription());
        generalAlert.alert(generalMessage);
    }

}
