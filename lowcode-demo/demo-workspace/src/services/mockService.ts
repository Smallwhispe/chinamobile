import { material, project } from '@alilc/lowcode-engine';
import { filterPackages } from '@alilc/lowcode-plugin-inject';
import { Message, Dialog } from '@alifd/next';
import { IPublicTypeProjectSchema, IPublicEnumTransformStage, IPublicModelPluginContext } from '@alilc/lowcode-types';
import DefaultPageSchema from './defaultPageSchema.json';
import DefaultI18nSchema from './defaultI18nSchema.json';

const apiBaseUrl = "http://localhost:8080/workschema";

const fetchData = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API request failed:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error("API request failed:", error);
    throw error; // 重新抛出错误以便在调用处处理
  }
};

const generateProjectSchema = (pageSchema, i18nSchema) => {
  return {
    componentsTree: [pageSchema],
    componentsMap: material.componentsMap,
    version: '1.0.0',
    i18n: i18nSchema,
  };
};

export const saveSchema = async (scenarioName = 'unknown', id, ctx) => {
  console.log('About to save schema to server. Scenario Name:', scenarioName, 'Project ID:', id);
  await setProjectSchemaToLocalStorage(scenarioName, id, ctx);
  await setPackagesToLocalStorage(scenarioName, id, ctx);
  Message.success('成功保存到服务器');
};

export const resetSchema = async (scenarioName = 'unknown') => {
  try {
    await new Promise((resolve, reject) => {
      Dialog.confirm({
        content: '确定要重置吗？您所有的修改都将消失！',
        onOk: () => resolve(),
        onCancel: () => reject(),
      });
    });
  } catch (err) {
    return;
  }

  const defaultSchema = generateProjectSchema(DefaultPageSchema, DefaultI18nSchema);
  project.importSchema(defaultSchema);
  project.simulatorHost?.rerender();

  console.log('About to reset schema. Scenario Name:', scenarioName);
  await setProjectSchemaToLocalStorage(scenarioName, "default", { project: { exportSchema: () => defaultSchema } });
  Message.success('成功重置页面');
};

const setProjectSchemaToLocalStorage = async (scenarioName, id, ctx) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }
  const schema = ctx.project.exportSchema(IPublicEnumTransformStage.Save);
  console.log("typeof-schema"+typeof(schema));

  console.log('Saving project schema. Scenario Name:', scenarioName, 'Project ID:', id, 'Data:', schema);
  await fetchData(`${apiBaseUrl}/saveProjectSchema`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      scenarioName,
      projectId: id,
      schemaJson: JSON.stringify(schema), // 确保这是字符串
    }),
  });

  console.log('Project Schema:', JSON.stringify(schema, null, 2));
};

const setPackagesToLocalStorage = async (scenarioName, id, ctx) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }

  const packages = await filterPackages(ctx.material.getAssets().packages);

  console.log('Saving packages. Scenario Name:', scenarioName, 'Project ID:', id, 'Data:', packages);
  await fetchData(`${apiBaseUrl}/savePackages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      scenarioName,
      projectId: id,
      packagesJson: JSON.stringify(packages), // 确保这是字符串
    }),
  });
};

export const getProjectSchemaFromLocalStorage = async (scenarioName, id) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }

  console.log('Fetching project schema. Scenario Name:', scenarioName, 'Project ID:', id);
  try {
    const response = await fetchData(`${apiBaseUrl}/getProjectSchema?scenarioName=${scenarioName}&projectId=${id}`, {
      method: 'GET',
    });
    console.log('Fetched project schema data:', response.schemaJson);
    console.log("typeofschema:"+typeof(response.schemaJson))
    const parsedSchema = JSON.parse(response.schemaJson);
    console.log("typeofschema:"+typeof(parsedSchema))
    return parsedSchema as any;
  } catch (error) {
    console.error('获取项目模式失败:', error);
    return undefined;
  }
};

export const getPackagesFromLocalStorage = async (scenarioName, id) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }

  console.log('Fetching packages. Scenario Name:', scenarioName, 'Project ID:', id);
  try {
    const response = await fetchData(`${apiBaseUrl}/getPackages?scenarioName=${scenarioName}&projectId=${id}`, {
      method: 'GET',
    });
   
    console.log("API Response:", response); // 这里输出整个响应
    console.log('Fetched packages data:', response.packagesJson);

    if (typeof response.packagesJson === 'string') {
      try {
        return JSON.parse(response.packagesJson) as any[];
      } catch (e) {
        console.error('解析 packages 字符串失败:', e, '原始数据:', response.packagesJson);
        return [];
      }
    } else if (Array.isArray(response.packagesJson)) {
      return response.packagesJson;
    } else {
      console.warn('响应数据中 packages 属性不是数组或未定义:', response.packagesJson);
      return [];
    }
  } catch (error) {
    console.error('获取数据失败:', error);
    return {};
  }
};


export const getResourceListFromLocalStorage = async (scenarioName) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }

  console.log('Fetching resource list. Scenario Name:', scenarioName);
  try {
    const response = await fetchData(`${apiBaseUrl}/getResourceList?scenarioName=${scenarioName}`, {
      method: 'GET',
    });
    console.log('Fetched resource list data:', response.list_json);
    if (typeof response.list_json === 'string') {
      try {
        // 尝试将字符串解析为数组
        return JSON.parse(response.list_json) as any[];
      } catch (e) {
        console.error('解析 packages 字符串失败:', e);
        return [];
      }
    } else if (Array.isArray(response.list_json)) {
      return response.list_json;
    } else {
      console.warn('响应数据中 packages 属性不是数组或未定义:', response.list_json);
      return [];
    }
    
  } catch (error) {
    console.error('获取资源列表失败:', error);
    return [{ "title": "首页", "slug": "index", "id": "index" }];
  }
};

export const setResourceListToLocalStorage = async (scenarioName, list) => {
  if (!scenarioName) {
    console.error('scenarioName is required!');
    return;
  }

  console.log('Saving resource list. Scenario Name:', scenarioName, 'Data:', list);
  await fetchData(`${apiBaseUrl}/saveResourceList`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ scenarioName, list_json: JSON.stringify(list) }),
  });
};

export const getProjectSchema = async (scenarioName = 'unknown',id) => {
  const pageSchema = await getPageSchema(scenarioName,id);
  return generateProjectSchema(pageSchema, DefaultI18nSchema);
};

export const getPageSchema = async (scenarioName = 'unknown', id) => {
  const pageSchemaResponse = await getProjectSchemaFromLocalStorage(scenarioName, id);
  const pageSchema = pageSchemaResponse?.componentsTree?.[0];
  console.log('pageschema 导入:', JSON.stringify(pageSchema, null, 2));
  return pageSchema || DefaultPageSchema;
};

export const getPreviewLocale = (scenarioName) => {
  return localStorage.getItem(`${scenarioName}:previewLocale`) || 'zh-CN';
};

export const setPreviewLocale = (scenarioName, locale) => {
  localStorage.setItem(`${scenarioName}:previewLocale`, locale || 'zh-CN');
  window.location.reload();
};
