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

  const [schema, setSchema] = useState()

  const [activeNav, setActiveNav] = useState()

  const scenarioName = getScenarioName();

  async function init() {
    const resourceList = await getResourceListFromLocalStorage(scenarioName);
    const allComponents = {};
    const allPackages = [];
    const libraryMap = {};
    for (const resource of resourceList) {
      const id = resource.id;
      const packages =await  getPackagesFromLocalStorage(scenarioName, id);
      const projectSchema = await  getProjectSchemaFromLocalStorage(scenarioName, id);

      // 处理 componentsMap 和其他数据
      const { componentsMap: componentsMapArray, componentsTree } = projectSchema;

      console.log('项目架构:', projectSchema);
      console.log('组件映射:', componentsMapArray);
      console.log('组件树:', componentsTree);
      componentsMapArray.forEach((component) => {
        allComponents[component.componentName] = component;
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
  const packages =await getPackagesFromLocalStorage(scenarioName, id);
  const projectSchema =await getProjectSchemaFromLocalStorage(scenarioName, id);
  const {
    componentsMap: componentsMapArray,
    componentsTree,
    i18n,
    dataSource: projectDataSource,
  } = projectSchema;

    console.log('componentsTree[0]:', JSON.stringify(componentsTree[0], null, 2));
    console.log('componentsTree:', JSON.stringify(componentsTree, null, 2));
    const pageSchema = componentsTree[0];
    
    setSchema(pageSchema);

    console.log('id', id, resourceList);
    setActiveNav(id);
    console.log('资源列表:', resourceList);
    console.log('组件:', components);


    setData({
      // schema: pageSchema,
      components,
      i18n,
      projectDataSource,
      resourceList,
    });
  }

  const { components, i18n = {}, projectDataSource = {} } = data as any;

  if (!schema || !components) {
    init();
    return <Loading fullScreen />;
  }
  const currentLocale = getPreviewLocale(getScenarioName());

  if (!(window as any).setPreviewLocale) {
    // for demo use only, can use this in console to switch language for i18n test
    // 在控制台 window.setPreviewLocale('en-US') 或 window.setPreviewLocale('zh-CN') 查看切换效果
    (window as any).setPreviewLocale = (locale:string) => setPreviewLocale(getScenarioName(), locale);
  }

  function customizer(objValue: [], srcValue: []) {
    if (isArray(objValue)) {
      return objValue.concat(srcValue || []);
    }
  }

  console.log('activeNav', activeNav);

  return (
    <div className="lowcode-plugin-sample-preview">         
      <Shell
        className={"iframe-hack"}
        device="desktop"
        style={{ border: "1px solid #eee" }}
      >
        <Shell.Branding>
          <div className="rectangular"></div>
          <span style={{ marginLeft: 10 }}>App Name</span>
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
                    const projectSchema =await getProjectSchemaFromLocalStorage(scenarioName, d.id);
                    console.log('setSchema', d.id, projectSchema?.componentsTree[0]);
                    setSchema(projectSchema?.componentsTree[0])
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
