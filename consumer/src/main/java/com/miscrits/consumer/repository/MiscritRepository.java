package com.miscrits.consumer.repository;

import com.miscrits.consumer.entity.MiscritEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MiscritRepository extends JpaRepository<MiscritEntity, Long> {

    long countByNameAndTargetMiscrit(String name, String targetMiscrit);

    long countByTargetMiscrit(String targetMiscrit);

    long countByHighGradeOrRareTrue();


    void upsertByActionId(Long actionId);

}
