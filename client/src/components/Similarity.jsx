import CardSimilarity from "./CardSimilarity";
import { useState, useEffect } from "react";
import logoFolha from '../assets/folhaLogo.png'
import logoGazeta from '../assets/gazetaLogo.png'
import logoG1 from '../assets/g1Logo.png'
import logoEstadao from '../assets/estadaoLogo.png'

function Similarity({similar}){
    const [folha, setFolha] = useState({})
    const [gazeta, setGazeta] = useState({});
    const [g1, setG1] = useState({});
    const [estadao, setEstadao] = useState({});

    useEffect(() => {
        for (let i in similar){
            if (i === 'folha_de_saopaulo'){
                setFolha({
                    'porcentagem':similar[i]['highest_tax'],
                    'link':similar[i]['data']['link_noticia'],
                    'titulo':similar[i]['data']['titulo_original'],
                    'subtitulo':similar[i]['data']['subtitulo_original']
                })
            }
            if (i === 'gazeta_do_povo'){
                setGazeta({
                    'porcentagem':similar[i]['highest_tax'],
                    'link':similar[i]['data']['link_noticia'],
                    'titulo':similar[i]['data']['titulo_original'],
                    'subtitulo':similar[i]['data']['subtitulo_original']
                })
            }
            if (i === 'g1'){
                setG1({
                    'porcentagem':similar[i]['highest_tax'],
                    'link':similar[i]['data']['link_noticia'],
                    'titulo':similar[i]['data']['titulo_original'],
                    'subtitulo':similar[i]['data']['subtitulo_original']
                })
            }
            if (i === 'estadao'){
                setEstadao({
                    'porcentagem':similar[i]['highest_tax'],
                    'link':similar[i]['data']['link_noticia'],
                    'titulo':similar[i]['data']['titulo_original'],
                    'subtitulo':similar[i]['data']['subtitulo_original']
                })
            }
        }
    },[similar])
    return(
        <div>
            <CardSimilarity response={folha} imgLogoSimilarity={logoFolha} altSimilarity="Logo Folha de São Paulo"/>
            <CardSimilarity response={gazeta} imgLogoSimilarity={logoGazeta} altSimilarity="Logo Gazeta do Povo"/>
            <CardSimilarity response={g1} imgLogoSimilarity={logoG1} altSimilarity="Logo G1"/>
            <CardSimilarity response={estadao} imgLogoSimilarity={logoEstadao} altSimilarity="Logo Estadão"/>
            <div className="bg-blue-500 w-[100%] h-[30px] mt-[20px]"></div>
        </div>
    )
}

export default Similarity