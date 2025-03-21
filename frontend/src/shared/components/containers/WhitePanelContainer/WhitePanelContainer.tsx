const WhitePanelContainer = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="bg-white h-fit w-full p-6 rounded-2xl shadow-black shadow flex-1 text-black">
      {children}
    </div>
  );
};

export default WhitePanelContainer;
