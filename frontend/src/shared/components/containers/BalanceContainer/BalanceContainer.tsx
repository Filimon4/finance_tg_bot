import React from "react";

const BalanceContainer = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex justify-center items-center w-full h-full">
      <div className="w-2/3 h-1 flex flex-col justify-center gap-4">
        {children}
      </div>
    </div>
  );
};

export default BalanceContainer;
