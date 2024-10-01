
import { IPublicTypeComponentMetadata, IPublicTypeSnippet } from '@alilc/lowcode-types';

const NewMaterialMeta: IPublicTypeComponentMetadata = {
  "componentName": "NewMaterial",
  "title": "NewMaterial",
  "docUrl": "",
  "screenshot": "",
  "devMode": "proCode",
  "npm": {
    "package": "diaohaoyu000",
    "version": "0.1.5",
    "exportName": "NewMaterial",
    "main": "src/index.tsx",
    "destructuring": true,
    "subName": ""
  },
  "configure": {
    "props": [
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "title",
            "zh-CN": "title"
          }
        },
        "name": "title",
        "setter": {
          "componentName": "StringSetter",
          "isRequired": false,
          "initialValue": ""
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "description",
            "zh-CN": "description"
          }
        },
        "name": "description",
        "setter": {
          "componentName": "StringSetter",
          "isRequired": false,
          "initialValue": ""
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "backgroundImage",
            "zh-CN": "backgroundImage"
          }
        },
        "name": "backgroundImage",
        "setter": {
          "componentName": "StringSetter",
          "isRequired": false,
          "initialValue": ""
        }
      }
    ],
    "supports": {
      "style": true
    },
    "component": {}
  }
};
const snippets: IPublicTypeSnippet[] = [
  {
    "title": "NewMaterial",
    "screenshot": "",
    "schema": {
      "componentName": "NewMaterial",
      "props": {}
    }
  }
];

export default {
  ...NewMaterialMeta,
  snippets
};
