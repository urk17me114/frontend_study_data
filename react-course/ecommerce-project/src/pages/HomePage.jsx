import {Header} from '../assets/components/Header.jsx'
import './HomePage.css'
import axios from "axios"
import { useEffect,useState } from 'react'
import { Money } from '../assets/utils/money.js' 



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
        <div className="products-grid">
            
            {products.map((product)=>{
                return(<>
                    <div key={product.id} className="product-container">
            <div className="product-image-container">
                {/* If the image is in the public folder, you do NOT need to import it. You can reference it directly using a URL */}
                <img className="product-image"
                src={product.image} />
            </div>

            <div className="product-name limit-text-to-2-lines">
                {product.name}
            </div>

            <div className="product-rating-container">
                <img className="product-rating-stars"
                src={`images/ratings/rating-${(product.rating.stars)*10}.png`} />
                <div className="product-rating-count link-primary">
                    {product.rating.count}
                </div>
            </div>

            <div className="product-price">
                ${ Money(product.priceCents)}
            </div>

            <div className="product-quantity-container">
                <select>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                </select>
            </div>

            <div className="product-spacer"></div>

            <div className="added-to-cart">
                <img src="images/icons/checkmark.png" />
                Added
            </div>

            <button className="add-to-cart-button button-primary">
                Add to Cart
            </button>
            </div>
                </>)

            })}
            

            </div>
        </div>
  </>
    )
}