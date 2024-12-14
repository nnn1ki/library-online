# client

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```


### Описание папок проекта

1. assets - статичные файлы, компоненты (фотографии, стили, шрифты)
2. components - переиспользуетмые компоненты (кнопки, списки и прочее)
3. views - стрницы (шаблоны страниц, "вьюшки")
4. router - конфигурация роутинка
5. services - api и другие сервисы 
6. utils - утилитарные функции (форматирования дат, валидации данных и т.д.)
7. 