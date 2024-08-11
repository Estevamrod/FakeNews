import CardSimilarity from "./CardSimilarity";
import { useState, useEffect } from "react";

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
            <CardSimilarity response={folha}/>
            <CardSimilarity response={gazeta}/>
            <CardSimilarity response={g1}/>
            <CardSimilarity response={estadao}/>
        </div>
    )
}

export default Similarity