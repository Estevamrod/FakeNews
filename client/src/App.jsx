import Navbar from "./components/Navbar"
import Date from "./components/Date"
import Similarity from "./components/Similarity"
import axios from 'axios'
import {useState} from 'react'
import logo from './assets/logo.svg'
import LoadingSpinner from "./components/Loading"

function App(){
    const [msg, setMsg] = useState("");
    const [date, setDate] = useState({});
    const [sentiment, setSentiment] = useState({});
    const [similarity, setSimilarity] = useState({});
    const [finished, setFinished] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const getdate = async() => {
        try {
            setIsLoading(true);
            const request = await axios.post('http://localhost:5000/v1/news', {
                'userQuery': msg
            })
            setDate(request.data.date);
            setSentiment(request.data.sentiment);
            setSimilarity(request.data.similarity);
            setFinished(true)
            setIsLoading(false);
        } catch (e) {
            console.log(e)
        }
    }
    return(
        <div>
            <Navbar/>
            <div className="flex justify-center items-center ">
            <img src={logo} alt="Logo Veracidade" className="flex justiy-center items-center w-[300px]"/>
            </div>
            {/* <Textbox/> */}
            <div>
                <div className="flex justify-center items-start content-center flex-wrap flex-col">
                    <span className="mt-[20px] text-blue-500">Manchete</span>
                    <div>
                        <input type='text' disabled={isLoading ? true : false} onChange={(event) => setMsg(event.target.value)} placeholder="Ex.: Vacina da Dengue do Instituto Butantan" className="rounded-[20px] w-[800px] mt-[10px] p-[15px] border-0 shadow-[0_8px_30px_rgb(0,0,0,0.12)]"/>
                        <button onClick={getdate} disabled={isLoading ? true : false} className="ml-[30px] font-black text-white bg-blue-500 p-[10px] rounded-full pr-[20px] pl-[20px] hover:bg-slate-50 hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[19px] hover:pr-[19px] transition">Pesquisar</button>
                    </div>
                </div>
                
            </div>
            {isLoading ?
                <div className="flex justify-center items-center" style={{"marginTop":"25px"}}>
                    <LoadingSpinner/>
                </div>
                :
                <div className="flex justify-center items-center flex-col">
                    <div className={finished ? "" : "hidden"}>
                        <div className="flex justify-center items-center flex-col mt-[20px]">
                            <h1 className="text-blue-500 text-[20px] mt-[20px]"><b>Datas e Sentimentos</b></h1>
                            <span className="text-center mb-[20px]">Datas de quando foram publicadas notícias parecidas com a manchete pesquisada anteriormente e sentimentos que a notícia transmite</span>
                            <Date dateRes={date} sentiment={sentiment}/>
                        </div>
                        <div className="flex justify-center items-center flex-col">
                            <h1 className="text-blue-500 text-[20px] mt-[30px]"><b>Similaridade</b></h1>
                            <span className="text-center mb-[20px]">Mostra noticias que sejam parecidas com a noticia buscada anteriormente e a média de similaridade entre elas.  </span>
                            <Similarity similar={similarity}/>
                        </div>
                    </div>
                </div>
            }
        </div>
    )
}

export default App