import BalanceContainer from '@shared/components/containers/BalanceContainer/BalanceContainer'
import { Mounth } from '@shared/components/Mounth/Mounth'

const Balance = () => {
  return (
    <BalanceContainer>
      <div className='flex flex-col'>
        <Mounth mounth='sdf' />
        <div className='flex flex-col'>
            <p>Баланс</p>
            <p>0</p>
        </div>
      </div>
      <hr className='w-full h-1 rounded-2xl bg-blue-200'/>
      <div className='flex flex-row w-full justify-between items-center'>
        <div className='flex flex-col'>
            <p>Баланс</p>
            <div className='flex flex-row justify-center gap-2'>
                <img src="" alt="" className='w-[40px] h-[30px]' />
                <p>0</p>
            </div>
        </div>
        <div className='flex flex-col'>
            <p>Баланс</p>
            <div className='flex flex-row justify-center gap-2'>
                <img src="" alt="" className='w-[40px] h-[30px]' />
                <p>0</p>
            </div>
        </div>
      </div>
    </BalanceContainer>
  )
}

export default Balance
