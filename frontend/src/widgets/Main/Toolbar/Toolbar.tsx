import { ToolCategories } from "@components/Toolbar/ToolCategories/ToolCategories";
import WhitePanelContainer from "@shared/components/containers/WhitePanelContainer/WhitePanelContainer";
import { useToolbarCategory } from "@shared/contexts/ToolbarCategory/useToolbarCategory";
import { ToolbarCategories } from "@shared/types/Toolbar";
import { useCallback } from "react";

const Toolbar = () => {
  const { currentCategory } = useToolbarCategory();

  const toolbarRouter = useCallback(() => {
    if (currentCategory == ToolbarCategories.overview) {
      return <>overview</>;
    } else if (currentCategory == ToolbarCategories.accounts) {
      return <>accounts</>;
    } else if (currentCategory == ToolbarCategories.history) {
      return <>history</>;
    } else if (currentCategory == ToolbarCategories.summary) {
      return <>summary</>;
    }
  }, [currentCategory]);

  return (
    <div className="h-full w-full flex flex-col gap-1">
      <ToolCategories />
      <WhitePanelContainer>{toolbarRouter()}</WhitePanelContainer>
    </div>
  );
};

export default Toolbar;
