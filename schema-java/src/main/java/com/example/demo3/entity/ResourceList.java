package com.example.demo3.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

import lombok.Getter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Entity
@Table(name = "resource_list")
public class ResourceList {
    private static final Logger logger = LoggerFactory.getLogger(ResourceList.class);

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Getter
    @Column(name = "scenario_name")
    private String scenarioName;

    @Getter
    @Column(columnDefinition = "json")
    private String list_json;

    private LocalDateTime created_at;
    private LocalDateTime updated_at;


    public void setList_json(String list_json) {
        this.list_json = list_json;
        logger.info("Resource list JSON updated: {}", list_json);
    }

    public void setScenarioName(String scenarioName) {
        this.scenarioName = scenarioName;
        logger.info("Scenario name updated: {}", scenarioName);
    }

    // Optionally, you can add timestamps if needed
    @PrePersist
    public void prePersist() {
        created_at = LocalDateTime.now();
        logger.info("ResourceList entity created at {}", created_at);
    }

    @PreUpdate
    public void preUpdate() {
        updated_at = LocalDateTime.now();
        logger.info("ResourceList entity updated at {}", updated_at);
    }
}
