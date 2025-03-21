import { ToolbarCategories } from "@shared/types/Toolbar";
import { createContext, useContext, useState } from "react";

const ToolbarCategoryContext = createContext<{
  currentCategory: ToolbarCategories;
  setCurrentCategory: (category: ToolbarCategories) => void;
}>({
  currentCategory: ToolbarCategories.overview,
  setCurrentCategory: () => {},
});

export const useToolbarCategory = () => useContext(ToolbarCategoryContext);

export const ToolbarCategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentCategory, setCurrentCategory] = useState<ToolbarCategories>(ToolbarCategories.overview);

  return (
    <ToolbarCategoryContext.Provider value={{ currentCategory, setCurrentCategory }}>
      {children}
    </ToolbarCategoryContext.Provider>
  );
};