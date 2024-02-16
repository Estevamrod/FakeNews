'use client'
import axios from "axios";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [Accuracy, setAccuracy] = useState("")
  const [Noticia, setNoticia] = useState("")
  const [Link, setLink] = useState("")

  const teste = () => {
    console.log(query)
    if (query !== "") {
      try{ 
        axios.post('http://localhost:1024/similar', {
          UserQuery: query
        }).then((value) => {
          console.log(value.data)
          setAccuracy(value.data.data.Accuracy)
          setNoticia(value.data.data.Noticia)
          setLink(value.data.data.Link)
        }).catch((e) => {
          console.log(e)
        })
      } catch (e) {
        console.log(e)
      }
    }
  }

  return (
    <div>
      <h1>Fake News</h1>
      <input placeholder="Digite aqui a noticia que te deixa em duvida..." type="text" onChange={(e) => setQuery(e.target.value)}/>
      <button onClick={teste}>Pesquisar</button>

      <div className="resultado">
        <span>Accuracy</span>
        <p style={{color: parseFloat(Accuracy.split("%")[0]) >= 50 ? "green" : "red"}}>{Accuracy}</p>
        <span>Noticia</span>
        <p>{Noticia}</p>
        <span>Link</span>
        <p>{Link}</p>
      </div>
    </div>
  );
}
