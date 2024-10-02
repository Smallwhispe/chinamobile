package com.example.demo3.controller;

import com.example.demo3.entity.ProjectSchema;
import com.example.demo3.entity.ResourceList;
import com.example.demo3.repository.ProjectSchemaRepository;
import com.example.demo3.repository.ResourceListRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@CrossOrigin(origins = "http://localhost:5556", allowCredentials = "true")
@RequestMapping("/workschema")
public class WorkSchemaController {

    @Autowired
    private ProjectSchemaRepository projectSchemaRepository;

    @Autowired
    private ResourceListRepository resourceListRepository;

    // 更新或插入项目模式和包数据
    @PostMapping("/saveProjectSchema")
    public String saveProjectSchema(@RequestBody ProjectSchema schema) {
        System.out.println("Received Project Schema: " + schema);

        Optional<ProjectSchema> existingSchema = projectSchemaRepository.findByScenarioNameAndProjectId(schema.getScenarioName(), schema.getProjectId());
        if (existingSchema.isPresent()) {
            ProjectSchema updateSchema = existingSchema.get();
            updateSchema.setSchemaJson(schema.getSchemaJson());
//            updateSchema.setPackagesJson(schema.getPackagesJson());
            projectSchemaRepository.save(updateSchema);
            System.out.println("Updated existing Project Schema: " + updateSchema);
            return "{\"status\": \"success\", \"message\": \"Updated existing Project Schema.\"}";
        } else {
            projectSchemaRepository.save(schema);
            System.out.println("Inserted new Project Schema: " + schema);
            return "{\"status\": \"success\", \"message\": \"Inserted new Project Schema.\"}";
        }
    }

    // 获取项目模式和包数据
    @GetMapping("/getProjectSchema")
    public ProjectSchema getProjectSchema(@RequestParam String scenarioName, @RequestParam String projectId) {
        System.out.println("Fetching Project Schema for Scenario: " + scenarioName + ", Project ID: " + projectId);
        return projectSchemaRepository.findByScenarioNameAndProjectId(scenarioName, projectId).orElse(null);
    }

    // 专门用于处理 packages_json 的 POST 请求
    @PostMapping("/savePackages")
    public String savePackages(@RequestBody ProjectSchema  packagesJson) {
        System.out.println("Received packages for Scenario: " + packagesJson);

        Optional<ProjectSchema> existingSchema = projectSchemaRepository.findByScenarioNameAndProjectId(packagesJson.getScenarioName(), packagesJson.getProjectId());
        if (existingSchema.isPresent()) {
            ProjectSchema updateSchema = existingSchema.get();
            updateSchema.setPackagesJson(packagesJson.getPackagesJson());
            projectSchemaRepository.save(updateSchema);
            System.out.println("Updated packages for existing Project Schema: " + updateSchema);
            return "{\"status\": \"success\", \"message\": \"Updated packages for existing Project Schema.\"}";
        } else {
            projectSchemaRepository.save(packagesJson);
            System.out.println("Inserted new Project Schema: " + packagesJson);
            return "{\"status\": \"success\", \"message\": \"Inserted new Project packages.\"}";
        }
    }

    // 专门用于处理 packages_json 的 GET 请求
    @GetMapping("/getPackages")
    public ProjectSchema getPackages(@RequestParam String scenarioName, @RequestParam String projectId) {
        System.out.println("Fetching packages for Scenario: " + scenarioName + ", Project ID: " + projectId);
//        ProjectSchema schema = projectSchemaRepository.findByScenarioNameAndProjectId(scenarioName, projectId).orElse(null);
//        return schema != null ? schema : "{\"status\": \"error\", \"message\": \"Packages not found.\"}";
        return projectSchemaRepository.findByScenarioNameAndProjectId(scenarioName, projectId).orElse(null);
    }

    @PostMapping("/saveResourceList")
    public String saveResourceList(@RequestBody ResourceList resourceList) {
        try {
            System.out.println("Received resource list: " + resourceList.getScenarioName() + ", Data: " + resourceList.getList_json());

            // 查找是否已存在相同的 scenarioName
            Optional<ResourceList> existingResourceList = resourceListRepository.findByScenarioName(resourceList.getScenarioName());

            if (existingResourceList.isPresent()) {
                // 更新现有的 ResourceList 的 list_json 字段
                ResourceList updateResourceList = existingResourceList.get();
                updateResourceList.setList_json(resourceList.getList_json());
                resourceListRepository.save(updateResourceList);
                System.out.println("Updated existing Resource List with scenarioName: " + resourceList.getScenarioName());
                return "{\"status\": \"success\", \"message\": \"Updated existing Resource List.\"}";
            } else {
                // 插入新的 ResourceList
                resourceListRepository.save(resourceList);
                System.out.println("Inserted new Resource List with scenarioName: " + resourceList.getScenarioName());
                return "{\"status\": \"success\", \"message\": \"Inserted new Resource List.\"}";
            }
        } catch (Exception e) {
            System.out.println("Error saving resource list: " + e.getMessage());
            return "{\"status\": \"error\", \"message\": \"Error saving resource list: " + e.getMessage() + "\"}";
        }
    }


    @GetMapping("/getResourceList")
    public ResourceList getResourceList(@RequestParam String scenarioName) {
        return resourceListRepository.findByScenarioName(scenarioName)
                .orElse(null);
    }
}
