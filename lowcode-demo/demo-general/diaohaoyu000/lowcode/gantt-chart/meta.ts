
import { IPublicTypeComponentMetadata, IPublicTypeSnippet } from '@alilc/lowcode-types';

const GanttChartMeta: IPublicTypeComponentMetadata = {
  "componentName": "GanttChart",
  "title": "GanttChart",
  "docUrl": "",
  "screenshot": "",
  "devMode": "proCode",
  "npm": {
    "package": "diaohaoyu000",
    "version": "0.1.7",
    "exportName": "GanttChart",
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
            "en-US": "jobs",
            "zh-CN": "jobs"
          }
        },
        "name": "jobs",
        "setter": {
          "componentName": "ArraySetter",
          "props": {
            "itemSetter": {
              "componentName": "StringSetter",
              "isRequired": false,
              "initialValue": ""
            }
          },
          "initialValue": []
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "startTimes",
            "zh-CN": "startTimes"
          }
        },
        "name": "startTimes",
        "setter": {
          "componentName": "ArraySetter",
          "props": {
            "itemSetter": {
              "componentName": "ObjectSetter",
              "props": {
                "config": {
                  "extraSetter": {
                    "componentName": "MixedSetter",
                    "isRequired": false,
                    "props": {}
                  }
                }
              },
              "isRequired": false,
              "initialValue": {}
            }
          },
          "initialValue": []
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "durations",
            "zh-CN": "durations"
          }
        },
        "name": "durations",
        "setter": {
          "componentName": "ArraySetter",
          "props": {
            "itemSetter": {
              "componentName": "NumberSetter",
              "isRequired": false,
              "initialValue": 0
            }
          },
          "initialValue": []
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "equipmentIds",
            "zh-CN": "equipmentIds"
          }
        },
        "name": "equipmentIds",
        "setter": {
          "componentName": "ArraySetter",
          "props": {
            "itemSetter": {
              "componentName": "StringSetter",
              "isRequired": false,
              "initialValue": ""
            }
          },
          "initialValue": []
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "rowHeight",
            "zh-CN": "rowHeight"
          }
        },
        "name": "rowHeight",
        "setter": {
          "componentName": "NumberSetter",
          "isRequired": false,
          "initialValue": 0
        }
      },
      {
        "title": {
          "label": {
            "type": "i18n",
            "en-US": "columnWidth",
            "zh-CN": "columnWidth"
          }
        },
        "name": "columnWidth",
        "setter": {
          "componentName": "NumberSetter",
          "isRequired": false,
          "initialValue": 0
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
    "title": "GanttChart",
    "screenshot": "",
    "schema": {
      "componentName": "GanttChart",
      "props": {}
    }
  }
];

export default {
  ...GanttChartMeta,
  snippets
};
