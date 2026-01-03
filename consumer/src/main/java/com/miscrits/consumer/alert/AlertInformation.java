package com.miscrits.consumer.alert;

public enum AlertInformation {

    CONSECUTIVE_FAILURES("Failed to find miscrit for multiple times consecutively!",
            "Failed to find miscrit for multiple times consecutively, " +
            "please take a look at the script and the game! " +
            "Character is most likely out of place, manually put character back into position."),

    CONSECUTIVE_CAPTURES("Consecutive capture detected! Capture Failed!!!",
            "Failed to capture miscrit. Do not be alarmed, you do not need to do anything or check on the game, this email " +
                    "will be repeatedly sent you to until the capture stage is timed out, the script will automatically continue normally " +
                    "after this failure, DO NOT DO ANYTHING. p.s. In the future, there may be a new mechanic to quickly resolve this issue"),

    EXCEPTION_MESSAGE("Something went wrong with the consumer service, please check.", "Consumer service stopped working, reason: "),

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
