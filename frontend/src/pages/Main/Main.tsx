import { MainContainer } from "@shared/components/containers/MainContainer/MainContainer";
import Toolbar from "@widgets/Main/Toolbar/Toolbar";
import Header from "@widgets/Main/Header/Header";
import Balance from "@widgets/Main/Balance/Balance";
import { ToolbarCategoryProvider } from "@shared/contexts/ToolbarCategory/useToolbarCategory";

const Main = () => {
  return (
    <ToolbarCategoryProvider>
      <MainContainer>
        <div className={`flex flex-col w-full h-full text-white`}>
          <Header />
          <div className="flex flex-col justify-between h-full">
            <div className="h-max flex-6">
              <Balance />
            </div>
            <div className="h-max flex-1/2 p-2">
              <Toolbar />
            </div>
          </div>
        </div>
      </MainContainer>
    </ToolbarCategoryProvider>
  );
};

export default Main;
