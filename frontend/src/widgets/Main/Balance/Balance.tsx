import BalanceContainer from "@shared/components/containers/BalanceContainer/BalanceContainer";
import { Mounth } from "@shared/components/Mounth/Mounth";
import styles from "./banalce.module.scss";
import { TbSquareRoundedArrowDown } from "react-icons/tb";
import { TbSquareRoundedArrowUp } from "react-icons/tb";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const Balance = () => {
  const { data } = useQuery({
    queryKey: ["balance"],
    queryFn: async () => {
      const res = await axios.get(
        `${import.meta.env.VITE_BACK_END_URL}/api/test/balance`
      );
      await new Promise((res) => setTimeout(() => res(true), 1500));
      return res;
    },
    staleTime: 60000,
  });

  return (
    <BalanceContainer>
      <Mounth mounth="Январь" />
      <div className="flex flex-col">
        <div className="flex flex-col items-center">
          <p className="text-[#E5D0ED]">Баланс</p>
          <>
            <p className="flex flex-row gap-1 font-bold text-[1.5rem] text-[#E5D0ED]">
              <span>{data?.data?.total || 0}</span>
              <span>{"Руб"}</span>
            </p>
          </>
        </div>
      </div>
      <div className="flex flex-col justify-center">
        <hr
          className={`w-full h-1 rounded-2xl ${styles.balanceDivider} border-0`}
        />
        <div className="flex flex-row w-full justify-between items-center text-[#664972]">
          <div className="flex flex-col">
            <p className="self-center">Баланс</p>
            <div className="flex flex-row justify-center gap-0.5 items-center">
              <TbSquareRoundedArrowDown
                size={25}
                width={"40px"}
                height={"30px"}
              />
              <>
                <p className="text-[1.3rem] self-center">
                  {data?.data?.expense || 0}
                </p>
              </>
            </div>
          </div>
          <div className="flex flex-col">
            <p className="self-center">Баланс</p>
            <div className="flex flex-row justify-center gap-0.5 items-center">
              <TbSquareRoundedArrowUp
                size={25}
                width={"40px"}
                height={"30px"}
              />
              <p className="text-[1.3rem] self-center">
                {data?.data?.income || 0}
              </p>
            </div>
          </div>
        </div>
      </div>
    </BalanceContainer>
  );
};

export default Balance;
