import ReactDOM from 'react-dom';
import React, { useState } from 'react';
import { Loading, Shell, Search, Nav } from '@alifd/next';
import mergeWith from 'lodash/mergeWith';
import isArray from 'lodash/isArray';
import { buildComponents, assetBundle, AssetLevel, AssetLoader } from '@alilc/lowcode-utils';
import ReactRenderer from '@alilc/lowcode-react-renderer';
import { injectComponents } from '@alilc/lowcode-plugin-inject';
import appHelper from './appHelper';
import { getProjectSchemaFromLocalStorage, getPackagesFromLocalStorage, getPreviewLocale, setPreviewLocale, getResourceListFromLocalStorage } from './services/mockService';

const getScenarioName = function () {
  if (location.search) {
    return new URLSearchParams(location.search.slice(1)).get('scenarioName') || 'general';
  }
  return 'general';
}

const SamplePreview = () => {
  const [data, setData] = useState({});
  const [schema, setSchema] = useState();
  const [activeNav, setActiveNav] = useState();
  const scenarioName = getScenarioName();

  async function init() {
    console.log('初始化数据...');
    const resourceList = await getResourceListFromLocalStorage(scenarioName);
    const allComponents = {};
    const allPackages = [];
    const libraryMap = {};
    let combinedDataSource = {}; // 初始化合并的 dataSource

    for (const resource of resourceList) {
      const id = resource.id;
      console.log(`加载资源 ID: ${id}`);
      const packages = await getPackagesFromLocalStorage(scenarioName, id);
      const projectSchema = await getProjectSchemaFromLocalStorage(scenarioName, id);

      const { componentsMap: componentsMapArray, componentsTree } = projectSchema;

      componentsMapArray.forEach((component) => {
        allComponents[component.componentName] = component;
      });

      componentsTree.forEach((schema) => {
        combinedDataSource = mergeWith(combinedDataSource, schema.dataSource || {}, customizer);
      });

      packages.forEach(({ package: _package, library, urls, renderUrls }) => {
        libraryMap[_package] = library;
        if (renderUrls) {
          allPackages.push(renderUrls);
        } else if (urls) {
          allPackages.push(urls);
        }
      });
    }

    // 加载所有资源
    const assetLoader = new AssetLoader();
    await assetLoader.load(allPackages);
    const components = await injectComponents(buildComponents(libraryMap, allComponents));

    const id = resourceList?.[0].id;
    const projectSchema = await getProjectSchemaFromLocalStorage(scenarioName, id);
    const { componentsTree } = projectSchema;

    const pageSchema = componentsTree[0];
    setSchema(pageSchema);
    setActiveNav(id);

    console.log('合并后的数据源:', combinedDataSource);
    setData({
      components,
      i18n: projectSchema.i18n || {},
      projectDataSource: combinedDataSource,
      resourceList,
    });
  }

  const { components, i18n = {}, projectDataSource = {} } = data;

  if (!schema || !components) {
    init();
    return <Loading fullScreen />;
  }
  const currentLocale = getPreviewLocale(getScenarioName());

  if (!(window as any).setPreviewLocale) {
    (window as any).setPreviewLocale = (locale: string) => setPreviewLocale(getScenarioName(), locale);
  }

  function customizer(objValue: [], srcValue: []) {
    if (isArray(objValue)) {
      return objValue.concat(srcValue || []);
    }
  }

  console.log('当前激活的导航:', activeNav);

  return (
    <div className="lowcode-plugin-sample-preview">         
      <Shell
        className={"iframe-hack"}
        device="desktop"
        style={{ border: "1px solid #eee" }}
      >
        <Shell.Branding>
          <div className="rectangular"></div>
          <span style={{ marginLeft: 10 }}></span>
        </Shell.Branding>
        <Shell.Navigation direction="hoz">
          <Search
            key="2"
            shape="simple"
            type="dark"
            palceholder="Search"
            style={{ width: "200px" }}
          />
        </Shell.Navigation>

        <Shell.Navigation>
          <Nav
            embeddable
            aria-label="global navigation"
            defaultSelectedKeys={[activeNav]}
          >
            {
              data?.resourceList?.map((d) => (
                <Nav.Item
                  key={d.id}
                  onClick={async () => {
                    const projectSchema = await getProjectSchemaFromLocalStorage(scenarioName, d.id);
                    console.log('设置当前 schema:', d.id, projectSchema?.componentsTree[0]);
                    setSchema(projectSchema?.componentsTree[0]);
                  }}
                  icon="account"
                >{d.title}</Nav.Item>
              ))
            }
          </Nav>
        </Shell.Navigation>

        <Shell.Content>
          <div style={{ minHeight: 1200, background: "#fff" }}>
          <ReactRenderer
            className="lowcode-plugin-sample-preview-content"
            schema={{
              ...schema,
              dataSource: mergeWith(schema.dataSource, projectDataSource, customizer),
            }}
            components={components}
            locale={currentLocale}
            messages={i18n}
            appHelper={appHelper}
          />
          </div>
        </Shell.Content>
      </Shell>
    </div>
  );
};

ReactDOM.render(<SamplePreview />, document.getElementById('ice-container'));
