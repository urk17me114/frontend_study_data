//import { useState } from 'react'
import './App.css'
import { Checkout } from './pages/checkout/Checkout.jsx'
import {HomePage} from './pages/home/HomePage.jsx'
import {Orders} from './pages/orders/Orders.jsx'
import {Tracking} from './pages/tracking.jsx'
import {Routes,Route} from 'react-router-dom'
import axios from "axios"
import { useEffect,useState } from 'react'


function App() {
  const [cart,setCart] = useState([]);
  useEffect(()=> 
    {axios.get('/api/cart-items?expand=product')//Here anything after ? is called the query paramter. It lets us ass additional info to our request
      .then((response)=>{setCart(response.data)})},[])

  return (
    <>
      <Routes> {/* Routes componenet tells React all the pages that are in the website */}
        
        {/* To add a page to the website we use route. Route is basically a page */}
        {/* Here index is same as giving path = "/" */}
        <Route index element = {<HomePage cart = {cart}/>}></Route> {/* Works like the url page in django */}
        <Route path = "checkout" element = {<Checkout cart = {cart}/>}></Route> {/* Works like the url page in django */}
        <Route path = "orders" element = {<Orders cart = {cart}/>}></Route> {/* Works like the url page in django */}
        <Route path = "tracking" element = {<Tracking/>}></Route> {/* Works like the url page in django */}
     
     </Routes> 
    </>
  )
}

export default App
