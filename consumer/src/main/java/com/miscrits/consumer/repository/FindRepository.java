package com.miscrits.consumer.repository;

import com.miscrits.consumer.entity.FindEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FindRepository extends JpaRepository<FindEntity, Long> {

    void deleteByActionId(Long actionId);

    long count();

    long countByIsSuccessfulTrue();
}
