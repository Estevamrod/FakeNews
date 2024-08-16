
function CardSimilarity({response}) {
  return (
    <div className="flex justify-center items-center flex-col bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] p-5 m-5">
    <div className="flex justify-center items-center flex-col md:flex-row lg:flex-row">
      <img
        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGRa3v94SfiR3CoFiBmhAs_PoXFJeOz3g1qw&s" alt="gazeta" className="w-1/2 lg:w-1/3 rounded-[30px] mb-4 lg:mb-0"/>
      <div className="flex flex-col gap-4 text-center lg:w-1/3">
        <div className="flex flex-col gap-1">
          <span className="font-bold text-blue-500">Título</span>
          {/* precisa atualizar aqui */}
          <span>{response ? response['titulo'] : ""}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="font-bold text-blue-500">Subtítulo</span>
          {/* precisa atualizar aqui */}
          <span className="">{response ? response['subtitulo'] : ""}</span>
        </div>
      </div>
      <div className="flex flex-col justify-center items-center lg:w-1/3">
        <span className="text-8xl font-bold mb-0 mt-5 text-yellow-300">{response ? response['porcentagem'] : ""}%</span>
        {/* precisa atualizar aqui */}
        <span className="text-yellow-500">Porcentagem de similaridade</span>
      </div>
      {/* Os links tambem precisam ser atualizados */}
      <a href={response ? response['link'] : "#"} target="_blank" className="flex justify-center items-center bg-blue-500 p-2 pr-3 pl-3 rounded-[30px] text-white mt-5 hover:bg-white hover:text-blue-500 hover:border-blue-500 hover:border-[1px] transition duration-300 lg:w-1/3 lg:hidden md:hidden"><b>Acesse aqui</b></a>
    </div>
    <a href={response ? response['link'] : "#"} target="_blank" className="flex justify-center items-center bg-blue-500 p-2 pr-3 pl-3 rounded-[30px] text-white mt-5 hover:bg-white hover:text-blue-500 hover:border-blue-500 hover:border-[1px] transition duration-300 text-center  lg:w-1/3 hidden lg:block md:block"><b>Acesse aqui</b></a>
    </div>
  );
}

export default CardSimilarity;