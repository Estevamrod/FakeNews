function CardSimilarity({response, imgLogoSimilarity, altSimilarity}) {
  return (
    <div className="flex justify-center items-center flex-col bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] p-5 m-5">
    <div className="flex justify-center items-center flex-col md:flex-row lg:flex-row">
      <img src={imgLogoSimilarity} alt={altSimilarity} className="w-1/2 lg:w-1/3 rounded-[30px] mb-4 lg:mb-0"/>
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
      <a href={response ? response['link'] : "#"} target="_blank" className="flex justify-center items-center bg-blue-500 p-[2px] pr-[3px] pl-[3px] rounded-[30px] text-white mt-5 hover:bg-white hover:text-blue-500 hover:border-blue-500 hover:border-[1px] hover:p-[1px] hover:pr-[2px] hover:pl-[2px] transition duration-300 lg:w-1/3 lg:hidden md:hidden"><b>Acesse aqui</b></a>
    </div>
    <button className="bg-blue-500 font-black text-white p-[10px] pr-[100px] pl-[100px] rounded-full m-[15px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[99px] hover:pr-[99px] transition"><a href={response ? response['link'] : "#"} target="_blank" >Clique para acessar</a></button>
    </div>
  );
}

export default CardSimilarity;