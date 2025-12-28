package com.miscrits.consumer.pojo;

@Data
public class Action {
    // todo refactor this to removeaction  prefix
    private Long actionNumber;
    private Boolean actionStatus;
    private String actionDescription;
    private String actionName;
    //TDOD get lombok and detelethis
    public Boolean getActionStatus() {
        return actionStatus;
    }
}
