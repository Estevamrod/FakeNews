import React from 'react';
import Navbar from './components/Navbar';

function Notfound() {
    return (
        <div>
            <Navbar/>
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                flexDirection: 'column',
                alignItems: 'center',
                height: '60vh',
                fontSize: '2rem'
            }}>
                Em desenvolvimento ☘️
            </div>
        </div>
    );
}

export default Notfound;