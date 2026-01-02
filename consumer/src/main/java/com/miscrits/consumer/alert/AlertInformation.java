package com.miscrits.consumer.alert;

public enum AlertInformation {

    CONSECUTIVE_FAILURES("Failed to find miscrit for multiple times consecutively!",
            "Failed to find miscrit for multiple times consecutively, " +
            "please take a look at the script and the game! " +
            "Character is most likely out of place, manually put character back into position."),

    GENERAL_MESSAGE("", "");

    public String body;

    public String title;

    AlertInformation(String title, String body) {
        this.title = title;
        this.body = body;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setBody(String body) {
        this.body = body;
    }
}
