import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p style={{'marginTop':'15px'}}>Carregando...</p>
    </div>
  );
};

export default LoadingSpinner;