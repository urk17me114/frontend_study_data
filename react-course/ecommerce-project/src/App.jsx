//import { useState } from 'react'
import './App.css'
import {HomePage} from './pages/HomePage.jsx'
import {Routes,Route} from 'react-router-dom'

function App() {
  

  return (
    <>
      <Routes> {/* Routes componenet tells React all the pages that are in the website */}
        
        {/* To add a page to the website we use route. Route is basically a page */}
        {/* Here index is same as giving path = "/" */}
        <Route index element = {<HomePage />}></Route> {/* Works like the url page in django */}
        <Route path = "checkout" element = {<div>Test checkout page </div>}></Route> {/* Works like the url page in django */}
     
     </Routes> 
    </>
  )
}

export default App
