import Card from "./CardDate";
import { useState, useEffect } from "react";

function Date({date_res}){
    const [folha, setFolha] = useState("")
    const [estadao, setEstadao] = useState("")
    const [gazeta, setGazeta] = useState("")
    const [g1, setG1] = useState("")

    useEffect(() => {
        for (let i in date_res) {
            if (i === 'folha_de_saopaulo') {
                console.log(i)
                setFolha(date_res[i]['datetime'])
            }
            if (i === 'gazeta_do_povo') {
                setGazeta(date_res[i]['datetime'])
            }
            if (i === 'g1') {
                setG1(date_res[i]['datetime'])
            }
            if (i === 'estadao') {
                setEstadao(date_res[i]['datetime'])
            }
        }
        console.log(date_res)
    },[date_res])

    return( 
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-4">
            <Card response={folha}/>
            <Card response={gazeta}/>
            <Card response={g1}/>
            <Card response={estadao} />
        </div>  
    )
}

export default Date