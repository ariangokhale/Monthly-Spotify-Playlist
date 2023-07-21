import React, { useState } from 'react';
import '../App.css';


function Login(props) {
    const handleLogin = async () => {
        try { 
        const response = await fetch('/');

        if (response.ok) {
            window.location.href = response.url;
        } else {
            console.error('Error initiating login:', response.statusText);
        }
        } catch (error) {
            console.error('Error initiating login:', error);
        }
    };
    return (
        <div className="LoginPage">
            <button onClick={handleLogin}> Log In</button>
        </div>
    );
};

export default Login;