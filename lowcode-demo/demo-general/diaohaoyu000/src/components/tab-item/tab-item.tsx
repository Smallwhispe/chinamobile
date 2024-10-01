import React, { useState, useEffect, useMemo, useCallback, createElement } from 'react';
import PropTypes from 'prop-types';
import { Component } from 'lowcode-lcc-comps';
import { Tab } from '@alifd/next';
import { createFetchHandler as __$$createFetchRequestHandler } from '@alilc/lowcode-datasource-fetch-handler';
import { create as __$$createDataSourceEngine } from '@alilc/lowcode-datasource-engine/runtime';
import '@alifd/next/lib/tab/style';
import './index.scss';

// 创建数据源配置的 hook
const useDataSourceEngine = (context) => {
  const dataSourceConfig = useMemo(() => ({
    list: [
      {
        options: () => ({
          headers: {},
          method: 'GET',
          isCors: true,
          params: {},
          uri: '/ass',
          timeout: 5000,
        }),
        id: '/ss',
        type: 'fetch',
        isInit: () => true,
      },
    ],
    sync: true,
  }), []);

  const [dataSourceEngine] = useState(() => __$$createDataSourceEngine(dataSourceConfig, context, {
    runtimeConfig: true,
    requestHandlersMap: { fetch: __$$createFetchRequestHandler() },
  }));

  return dataSourceEngine;
};

const TabItem = ({ style, className }) => {
  const [state, setState] = useState({ hello: 'world' });
  const dataSourceEngine = useDataSourceEngine({});

  // 处理数据源重新加载
  const reloadDataSource = useCallback(async () => {
    await dataSourceEngine.reloadDataSource();
  }, [dataSourceEngine]);

  // 模拟 componentDidMount 和 componentDidUpdate
  useEffect(() => {
    reloadDataSource();
    console.log('componentDidMount-----');

    return () => {
      console.log('componentWillUnmount');
    };
  }, [reloadDataSource]);

  // 处理组件捕获错误
  useEffect(() => {
    const handleError = (error) => {
      console.log('componentDidCatch');
    };

    // 这里只是模拟，React 的 Error Boundary 需要用到 class component
    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);

  // 处理点击事件
  const handleClick = () => {
    console.log('onClick');
  };

  return (
    <Component
      className="component_k8e4naln"
      style={style}
      cls={className}
      fieldId="symbol_k8bnubw4"
    >
      <Tab
        shape="pure"
        size="medium"
        excessMode="slide"
        needBadge={false}
        items={[
          { title: 'Tab1', primaryKey: 'node_ocm0xcl7hf2' },
          { title: 'Tab2', primaryKey: 'node_ocm0xcl7hf3' },
          { title: 'Tab3', primaryKey: 'node_ocm0xcl7hf4' },
        ]}
        unmountInactiveTabs={false}
      >
        <Tab.Item title="Tab1" primaryKey="node_ocm0xcl7hf2" />
        <Tab.Item title="Tab2" primaryKey="node_ocm0xcl7hf3" />
        <Tab.Item title="Tab3" primaryKey="node_ocm0xcl7hf4" />
      </Tab>
    </Component>
  );
};

TabItem.propTypes = {
  style: PropTypes.object,
  className: PropTypes.string,
};

TabItem.defaultProps = {
  style: {},
  className: '',
};

export default TabItem;
