function Textbox(){
    return(
        <div>
        <div className="flex justify-center items-start content-center flex-wrap flex-col">
            <span className="mt-[20px] text-blue-500">Manchete</span>
            <input type="text" placeholder="Ex.: Vacina da dengue do butantan" className="rounded-[20px] w-[75%] mt-[10px] p-[15px] border-0 shadow-[0_8px_30px_rgb(0,0,0,0.12)]"/>
        </div>
        <div className="hidden justify-center items-start content-center flex-wrap flex-col">
             <span className="mt-[20px] text-blue-500">Trecho da notícia</span>
            <textarea type="text" placeholder="Ex.: Vacina da dengue do butantan" className="rounded-[20px] w-[75%] mt-[10px] p-[15px] shadow-[0_8px_30px_rgb(0,0,0,0.12)]"/>
        </div>
        </div>
    )
}

export default Textbox