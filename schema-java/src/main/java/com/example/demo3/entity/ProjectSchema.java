package com.example.demo3.entity;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.Objects;

@Entity
@Table(name = "project_schema")
public class ProjectSchema {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Setter
    @Getter
    @Column(name = "scenario_name")
    private String scenarioName;
    @Setter
    @Getter
    @Column(name = "project_id")
    private String projectId;

    @Setter
    @Getter
    @Column(name = "schema_json",columnDefinition = "json")
    private String schemaJson;

    @Setter
    @Getter
    @Column(name = "packages_json",columnDefinition = "json")
    private String packagesJson;

    @Column(name = "preview_locale")
    private String previewLocale;

    private LocalDateTime created_at;
    private LocalDateTime updated_at;

    // Getters and setters
    public int getId() {
        return Math.toIntExact(id);
    }

    public void setId(int id) {
        this.id = (long) id;
    }

    public String getPreviewLocale() {
        return previewLocale;
    }

    public void setPreviewLocale(String previewLocale) {
        this.previewLocale = previewLocale;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass()!= o.getClass()) return false;
        ProjectSchema that = (ProjectSchema) o;
        return id == that.id && Objects.equals(scenarioName, that.scenarioName) && Objects.equals(projectId, that.projectId) && Objects.equals(schemaJson, that.schemaJson) && Objects.equals(packagesJson, that.packagesJson) && Objects.equals(previewLocale, that.previewLocale);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, scenarioName, projectId, schemaJson, packagesJson, previewLocale);
    }
}

