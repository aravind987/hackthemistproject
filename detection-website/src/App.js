

import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React from 'react'
import ReactDOM from 'react-dom'

import {Home, Profile} from './pages/import.js'


function App() {

   return (
        <div>
            <BrowserRouter>

                  <Routes>

                    <Route path="/" element={<Home/>}/>

                  </Routes>

            </BrowserRouter>
        </div>

   )
}

export default App;