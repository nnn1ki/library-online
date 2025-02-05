import pluginVue from 'eslint-plugin-vue'
import {
  defineConfigWithVueTs,
  vueTsConfigs,
} from '@vue/eslint-config-typescript'
import skipFormattingConfig from "@vue/eslint-config-prettier/skip-formatting";
export default defineConfigWithVueTs(
  {
    languageOptions: {
        ecmaVersion: "latest",
        sourceType: "script",
    },
  },
  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  skipFormattingConfig
);