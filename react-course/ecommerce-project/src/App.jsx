//import { useState } from 'react'
import './App.css'
import { Checkout } from './pages/Checkout.jsx'
import {HomePage} from './pages/HomePage.jsx'
import {Orders} from './pages/Orders.jsx'
import {Tracking} from './pages/tracking.jsx'
import {Routes,Route} from 'react-router-dom'
import axios from "axios"
import { useEffect,useState } from 'react'


function App() {
  const [cart,setCart] = useState([]);
  useEffect(()=>{axios.get('/api/cart-items').then((response)=>{
            setCart(response.data)})},[])

  return (
    <>
      <Routes> {/* Routes componenet tells React all the pages that are in the website */}
        
        {/* To add a page to the website we use route. Route is basically a page */}
        {/* Here index is same as giving path = "/" */}
        <Route index element = {<HomePage cart = {cart}/>}></Route> {/* Works like the url page in django */}
        <Route path = "checkout" element = {<Checkout cart = {cart}/>}></Route> {/* Works like the url page in django */}
        <Route path = "orders" element = {<Orders/>}></Route> {/* Works like the url page in django */}
        <Route path = "tracking" element = {<Tracking/>}></Route> {/* Works like the url page in django */}
     
     </Routes> 
    </>
  )
}

export default App
