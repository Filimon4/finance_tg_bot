import { ToolCategories } from "@components/Toolbar/ToolCategories/ToolCategories"

const Toolbar = () => {
  return (
    <>
      <div className='h-full w-full flex flex-col gap-1'>
        <ToolCategories />
        <div className='bg-white h-fit w-full p-6 rounded-2xl shadow-gray-500 shadow flex-1'>
          
        </div>
      </div>
    </>
  )
}

export default Toolbar