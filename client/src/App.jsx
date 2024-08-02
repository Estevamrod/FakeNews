import Navbar from "./components/Navbar"
import Textbox from "./components/Textbox"
import Date from "./components/Date"
import Similarity from "./components/Similarity"

function App(){
    return(
        <div>
             <Navbar/>
             <h1 className="flex justify-center items-center text-2xl text-blue-500"><b>VERACIDADE</b></h1>
            <Textbox/>
            <div className="flex justify-center items-center flex-col">
            <div className="hidden">
            <h1 className="text-blue-500 text-[20px] mt-[20px]"><b>Datas e Sentimentos</b></h1>
            <span className="text-center">Datas de quando foram publicadas notícias parecidas com a manchete pesquisada anteriormente e sentimentos que a notícia transmite</span>
            <Date/>
            <h1 className="text-blue-500 text-[20px] mt-[20px]"><b>Similaridade</b></h1>
            <span className="text-center">Mostra noticias que sejam parecidas com a noticia buscada anteriormente e a média de similaridade entre elas.  </span>
            <Similarity/>
            </div>
            </div>
            
        </div>
       
    )
}

export default App