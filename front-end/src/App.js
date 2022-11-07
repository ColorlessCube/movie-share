import React from 'react';
import './App.css';
import Recent from "./components/recent";
import PageLayout from './pages/Layout'
import Login from './pages/Login'
import {BrowserRouter, Routes, Route} from 'react-router-dom'

function App() {
    return (
        // 路由配置
        <BrowserRouter>
            <div className="App">
                <Routes>
                    <Route path='/' element={<PageLayout/>}>
                        <Route path='recent-watch' element={<Recent/>}/>
                    </Route>
                    <Route path='/login' element={<Login/>}/>
                </Routes>
            </div>
        </BrowserRouter>
    );
}

export default App;
