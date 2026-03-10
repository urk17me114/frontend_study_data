//import { useState } from 'react'
import './App.css'
import { Checkout } from './pages/Checkout.jsx'
import {HomePage} from './pages/HomePage.jsx'
import {Orders} from './pages/Orders.jsx'
import {Tracking} from './pages/tracking.jsx'
import {Routes,Route} from 'react-router-dom'


function App() {
  

  return (
    <>
      <Routes> {/* Routes componenet tells React all the pages that are in the website */}
        
        {/* To add a page to the website we use route. Route is basically a page */}
        {/* Here index is same as giving path = "/" */}
        <Route index element = {<HomePage />}></Route> {/* Works like the url page in django */}
        <Route path = "checkout" element = {<Checkout/>}></Route> {/* Works like the url page in django */}
        <Route path = "orders" element = {<Orders/>}></Route> {/* Works like the url page in django */}
        <Route path = "tracking" element = {<Tracking/>}></Route> {/* Works like the url page in django */}
     
     </Routes> 
    </>
  )
}

export default App
