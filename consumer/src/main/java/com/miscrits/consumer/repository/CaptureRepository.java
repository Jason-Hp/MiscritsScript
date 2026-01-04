package com.miscrits.consumer.repository;

import com.miscrits.consumer.entity.CaptureEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface CaptureRepository extends JpaRepository<CaptureEntity, Long> {

    long count();

    long countByCapturedTrue();

    @Query("SELECT c.miscritName from CaptureEntity c")
    List<String> findAllCapturedMiscritNames();

    CaptureEntity getByActionId(Long actionId);

    //TODO once script is upgraded to be able to catch target miscrit autonomously, add get is target miscrit captured + count

}
