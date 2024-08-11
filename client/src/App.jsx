import Navbar from "./components/Navbar"
import Date from "./components/Date"
import Similarity from "./components/Similarity"
import axios from 'axios'
import {useState} from 'react'

function App(){
    const [msg, setMsg] = useState("");
    const [date_res, setData_res] = useState({});
    const getdate = async() => {
        try {   
            const dateReq = await axios.post('http://localhost:5000/v1/date', {
                'userQuery': msg
            })
            setData_res(dateReq.data)
        } catch (e) {
            console.log(e)
        }
    }
    return(
        <div>
            <Navbar/>
            <h1 className="flex justify-center items-center text-2xl text-blue-500"><b>VERACIDADE</b></h1>
            {/* <Textbox/> */}
            <div>
                <div className="flex justify-center items-start content-center flex-wrap flex-col">
                    <span className="mt-[20px] text-blue-500">Manchete</span>
                    <input type="text" onChange={(event) => setMsg(event.target.value)} placeholder="Ex.: Vacina da dengue do butantan" className="rounded-[20px] w-[75%] mt-[10px] p-[15px] border-0 shadow-[0_8px_30px_rgb(0,0,0,0.12)]"/>
                </div>
                <button onClick={getdate}>PESQUISA</button>
            </div>
            <div className="flex justify-center items-center flex-col">
            <div>
                <h1 className="text-blue-500 text-[20px] mt-[20px]"><b>Datas e Sentimentos</b></h1>
                <span className="text-center">Datas de quando foram publicadas notícias parecidas com a manchete pesquisada anteriormente e sentimentos que a notícia transmite</span>
                <Date date_res={date_res}/>
                <h1 className="text-blue-500 text-[20px] mt-[20px]"><b>Similaridade</b></h1>
                <span className="text-center">Mostra noticias que sejam parecidas com a noticia buscada anteriormente e a média de similaridade entre elas.  </span>
                <Similarity/>
            </div>
            </div>
        </div>
    )
}

export default App