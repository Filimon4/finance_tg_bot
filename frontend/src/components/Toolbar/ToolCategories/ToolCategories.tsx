import { useToolbarCategory } from "@shared/contexts/ToolbarCategory/useToolbarCategory";
import { ToolbarCategories, ToolbarCategoriesNames } from "@shared/types/Toolbar";

export const ToolCategories = () => {
  const { currentCategory, setCurrentCategory } = useToolbarCategory();

  return (
    <div className="flex flex-row justify-between items-center px-4 cursor-pointer">
      {Object.entries(ToolbarCategoriesNames).map(([category, name], i) => (
        <div key={i} className="text-black" onClick={() => setCurrentCategory(category as ToolbarCategories)} >
          <p>{name}</p>
        </div>
      ))}
    </div>
  );
};
