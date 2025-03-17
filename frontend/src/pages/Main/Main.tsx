import Balance from "@components/Main/components/Balance";
import styles from "./main.module.scss";
import Header from "@components/Main/components/Header";
import Toolbar from "@components/Main/components/Toolbar";

const Main = () => {
  return (
    <div className={`flex flex-col w-screen h-screen ${styles.main} text-white`}>
      <Header />
      <div className="flex flex-col justify-between">
        <Balance />
        <Toolbar />
      </div>
    </div>
  );
};

export default Main;
