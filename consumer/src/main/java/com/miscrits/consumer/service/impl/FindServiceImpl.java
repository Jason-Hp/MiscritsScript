package com.miscrits.consumer.service.impl;

import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.pojo.Action;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;

@Service
public class FindServiceImpl implements com.miscrits.consumer.service.Service {

    //todo find this constant with research in mis discrod
    private final int SIZE_OF_QUEUE = 5;

    //todo USE ATOMIC HEAP ACCESSIBLE MEMORY HERE (STACK STRUCT), LATER CHANGE TO DB
    private Queue<Action> previousFinds = new LinkedBlockingQueue<>(SIZE_OF_QUEUE);

    //todo in config
    @Autowired
    private Map<String, Alert> alertMap;

    @Override
    public String key() {
        return "find";
    }

    @Override
    public void operate(String value) {
        // TODO use GSON here to convert value to Action pojo
        Action findAction =;

        // look through past SIZE_OF_QUEUE finds
        AtomicBoolean failedAll = new AtomicBoolean(true);

        if (!findAction.getActionStatus()) {
            previousFinds.forEach(previousFind -> {
                if (previousFind.getActionStatus()) {
                    failedAll.set(false);
                }
            });
        }
        if (failedAll.get()) {
            // todo Alert service
            Alert alert = alertMap.get("error");
            if (alert != null) {
                alert.alert(findAction.get);
            }
            return;
        }
        previousFinds.offer(findAction);
    }

}
