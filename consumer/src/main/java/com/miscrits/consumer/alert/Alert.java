package com.miscrits.consumer.alert;

public interface Alert {

    String type();

    void alert(AlertInformation alertInformation);

    String formatSubject(String title);

    String formatMessage(String message);

}
