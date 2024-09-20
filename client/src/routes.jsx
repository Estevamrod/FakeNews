import React from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import App from './App.jsx'
import LandingPage from "./landingpage.jsx";
import Notfound from "./Notfound.jsx";

const Roteamento = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={ <App/> } path="/" exact/>
                <Route element={ <LandingPage/> } path="/sobre" />
                <Route element={ <Notfound/> } path="/noticias"/>
            </Routes>
        </BrowserRouter>
    )
}

export default Roteamento