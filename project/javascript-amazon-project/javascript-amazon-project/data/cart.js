

/* export const cart = []; */
export let cart = JSON.parse(localStorage.getItem("key")); /* To convert string to array */

if(!cart){
cart = [
  
{
  id: "e43638ce-6aa0-4b85-b27f-e1d07eb678c6",
  name: "Black and Gray Athletic Cotton Socks - 6 Pairs",
  quantity:1,
  deliveryOptionId: "1"
  },
  {
  id: "3ebe75dc-64d2-4137-8860-1f5a963e534b",
  name: "6 Piece White Dinner Plate Set",
  quantity:1,
  deliveryOptionId: "2"
}
]}

/* To make it a module
first export the variable that is to be used in other js
import the variable using the syntax import {variable name} from "file location"
in html file in script like how u define classes give type="module" */


export function addToCart(productID,productName){
  /* Logic : Check the cart → if item exists, increase quantity in cart → otherwise add it in matchingItem.” */

  let matchingItem;
    
    if (cart.forEach((value)=>{
      if (productID===value.id){
        matchingItem=value;

      }
}));
    
    if(matchingItem){
        matchingItem.quantity+=1;
    }
    else{
      cart.push({
        id: productID,
        name:productName,
        quantity:1,
        deliveryOptionId: "1"
      });
    }
    saveToStorage();
}

export function removeFromCart(product_id){
  const newCart = [];
  cart.forEach((value)=>{
    if(value.id!==product_id){
      newCart.push(value); 
    }
  })
  cart = newCart;
  saveToStorage();
}

//Here we need to add a local storage as the variable gets resetted when a new page is loaded
//Local storage can only save strings

function saveToStorage(){
  localStorage.setItem("key",JSON.stringify(cart));
}

export function updateDeliveryOption(productID,deliveryOptionId){
  let matchingItem;
  cart.forEach((value)=>{
    if (productID===value.id){
        matchingItem=value;

      }
});
  
matchingItem.deliveryOptionId=deliveryOptionId;
saveToStorage();
}