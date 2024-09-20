function CardDate({date, sentiment, imgLogoDate, altDate}){
    return(
        <div className="flex justify-center items-center flex-col min-w-60 max-w-sm bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] w-10 p-4 m-2">
            <img src={imgLogoDate} alt={altDate} className="w-32 rounded-[30px]"/>
            <h1 className="mt-[2vh] text-blue-500 text-center"><b>Data da Publicação</b></h1>
            <span>{date ? date : ""}</span>
            <span className="mt-[1vh] text-blue-500 flex flex-col"><b>Sentimentos</b></span>

            <div className="grid grid-rows-3 grid-flow-col gap-x-3">
                <div className="">Positivo:</div>
                <div className="">Neutro:</div>
                <div className="">Negativo:</div>
                <div className="">{sentiment ? sentiment['positivo'] : "0%"}</div>
                <div className="">{sentiment ? sentiment['neutro'] : "0%"}</div>
                <div className="">{sentiment ? sentiment['negativo'] : "0%"}</div>
            </div>
        </div>
    )
}

export default CardDate