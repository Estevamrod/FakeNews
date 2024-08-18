import Card from "./CardDate";
import { useState, useEffect } from "react";
import logo from '../assets/logo.svg'
import logoFolha from '../assets/folhaLogo_date.png'
import logoGazeta from '../assets/gazetaLogo_date.png'
import logoG1 from '../assets/g1Logo_date.png'
import logoEstadao from '../assets/estadaoLogo_date.png'


function Date({dateRes, sentiment}){
    const [folha, setFolha] = useState("")
    const [estadao, setEstadao] = useState("")
    const [gazeta, setGazeta] = useState("")
    const [g1, setG1] = useState("")

    

    useEffect(() => {
        for (let i in dateRes){
            if (i === 'folha_de_saopaulo'){
                setFolha(dateRes[i]['datetime'])
            }
            if (i === 'gazeta_do_povo'){
                setGazeta(dateRes[i]['datetime'])
            }
            if (i === 'g1'){
                setG1(dateRes[i]['datetime'])
            }
            if (i === 'estadao'){
                setEstadao(dateRes[i]['datetime'])
            }
        }
    },[dateRes, sentiment])

    


    return( 
        

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-4">
            <Card date={folha} sentiment={sentiment['folha_de_saopaulo']} imgLogoDate={logoFolha} altDate="Logo Folha de São Paulo"/>
            <Card date={gazeta} sentiment={sentiment['gazeta_do_povo']} imgLogoDate={logoGazeta} altDate="Logo Gazeta do Povo"/>
            <Card date={g1} sentiment={sentiment['g1']} imgLogoDate={logoG1} altDate="Logo G1"/>
            <Card date={estadao} sentiment={sentiment['estadao']} imgLogoDate={logoEstadao} altDate="Logo Estadao"/>
        </div>  
    )
}

export default Date