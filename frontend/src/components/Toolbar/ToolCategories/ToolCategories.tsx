const data = ["Обзор", "История", "Резюме", "Счета"]

export const ToolCategories = () => {
  return (
    <div className='flex flex-row justify-between items-center px-4 cursor-pointer'>
      {data.map((name, i) => (
        <div key={i} className= 'text-black'>
          <p>{name}</p>
        </div>
      ))}
    </div>
  )
}