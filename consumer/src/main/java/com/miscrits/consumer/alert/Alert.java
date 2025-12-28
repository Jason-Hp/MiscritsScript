package com.miscrits.consumer.alert;

public interface Alert {

    String type();

    void alert(String message, String title);

    String formatSubject(String title);

    String formatMessage(String message);

}
