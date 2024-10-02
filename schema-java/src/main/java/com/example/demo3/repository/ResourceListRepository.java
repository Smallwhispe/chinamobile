package com.example.demo3.repository;

import com.example.demo3.entity.ResourceList;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ResourceListRepository extends JpaRepository<ResourceList, Long> {
    Optional<ResourceList> findByScenarioName(String scenarioName);
}