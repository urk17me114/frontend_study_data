import {Header} from '../../assets/components/Header.jsx'
import './HomePage.css'
import axios from "axios"
import { useEffect,useState } from 'react'
import { ProductsGrid } from './ProductsGrid.jsx'




export function HomePage({cart}){
    
    /* //fetch is asynchronous so u have to use then
    //response .json() is asynchronous so u have to use then
    
    
    //axios is a cleaner way to make requests to the backend
    fetch('http://localhost:3000/api/products').then((response)=>{  // To fetch the data from the backend
        return response.json()}).then((data)=>{
            console.log(data);
        })

     // To fetch the data from the backend */

    const [products,setProducts] = useState([]); //iniially the products array is set to []
    

    useEffect (()=>{axios.get('http://localhost:3000/api/products').then((response)=>{  // To fetch the data from the backend   
        setProducts(response.data); /* here data is the inbiult ppty of axios */
        })},[]) //Here [] is called the dependency array

    /* The issue here is everytime u call the homepage the data from the backend is loaded again. But we only have to d it once. so 
    for that we use "useEffect" */
    
    return(
    <>    
        <title>Ecommerce Project</title>
        
       
        <Header cart= {cart}/>
        
        <div className="home-page">
            <ProductsGrid products = {products}/>
        </div>
        
  </>
    )
}