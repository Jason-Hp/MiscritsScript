package com.miscrits.consumer.aspect;

import com.miscrits.consumer.alert.Alert;
import com.miscrits.consumer.alert.AlertInformation;
import lombok.AllArgsConstructor;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
@AllArgsConstructor
public class ExceptionAspect {

    private final Alert errorAlertImpl;

    @AfterThrowing(
            pointcut = "within(com.miscrits.consumer..*)",
            throwing = "ex"
    )
    public void alertOnException(JoinPoint jp, Throwable ex) {
        AlertInformation exceptionMessage = AlertInformation.EXCEPTION_MESSAGE;
        exceptionMessage.setBody(exceptionMessage.body + ex.getMessage());
        errorAlertImpl.alert(exceptionMessage);
    }

}
