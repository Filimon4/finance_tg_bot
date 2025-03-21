
export enum ToolbarCategories {
  overview = 'overview',
  history = 'history',
  summary = 'summary',
  accounts = 'accounts'
}

export const ToolbarCategoriesNames: {
  [k in ToolbarCategories]: string
} = {
  [ToolbarCategories.accounts]: "Счета",
  [ToolbarCategories.history]: "История",
  [ToolbarCategories.overview]: "Обзор",
  [ToolbarCategories.summary]: "Резюме",
}
