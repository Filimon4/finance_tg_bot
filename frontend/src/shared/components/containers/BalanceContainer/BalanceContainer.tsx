

import React from 'react'

const BalanceContainer = ({children}: {children: React.ReactNode}) => {
  return (
    <div className='flex justify-center items-center w-full h-full'>
        <div className='w-full h-full'>
            {children}
        </div>
    </div>
  )
}

export default BalanceContainer
