import { IPublicModelPluginContext } from '@alilc/lowcode-types';
import { injectAssets } from '@alilc/lowcode-plugin-inject';
import assets from '../../services/assets.json';
import { getProjectSchema } from '../../services/mockService';

const EditorInitPlugin = (ctx: IPublicModelPluginContext) => {
  return {
    async init() {
      const { material, project, config, editorWindow } = ctx;
      const scenarioName = config.get('scenarioName');

      // 设置物料描述
      await material.setAssets(await injectAssets(assets));

      const schema = await getProjectSchema(scenarioName, editorWindow.resource?.options.id);
      // 加载 schema
      if (schema) {
        project.importSchema(schema as any);
        console.log('schema 已成功导入:', JSON.stringify(schema, null, 2));

        // console.log('schema 已成功导入');
        // // 监听模拟器主机准备好事件
        //   if (project.simulatorHost) {
        //     project.simulatorHost.rerender();
        //     console.log('页面已重新渲染');
        //   } else {
        //     console.warn('模拟器主机未定义，无法重新渲染页面');
        //   }
      }else {
        console.warn('导入 schema 失败，使用默认 schema');
      }
    },
  };
}

EditorInitPlugin.pluginName = 'EditorInitPlugin';
EditorInitPlugin.meta = {};
export default EditorInitPlugin;