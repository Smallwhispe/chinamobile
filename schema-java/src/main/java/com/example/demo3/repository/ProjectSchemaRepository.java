package com.example.demo3.repository;
import com.example.demo3.entity.ProjectSchema;
import com.example.demo3.entity.ResourceList;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ProjectSchemaRepository extends JpaRepository<ProjectSchema, Long> {
    Optional<ProjectSchema> findByScenarioNameAndProjectId(String scenarioName, String projectId);
}


