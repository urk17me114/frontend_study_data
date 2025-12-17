import {cart,removeFromCart} from "../data/cart.js"
import { products } from "../data/products.js";
import { formatCurrency} from "./utils/money.js";

let checkout = "";
cart.forEach((value)=>{
    const productID = value.id;
    
    let matchingProduct;   //if the productID in cart matches with the id of products then store all the respective
    products.forEach((product)=>{   //details into a reference called matchingProduct
        if (product.id ===  productID){
            matchingProduct=product;
        }
    });


    const html1 = 
        `<div class="cart-item-container js-cart-item-container-${matchingProduct.id}">
            <div class="delivery-date">
              Delivery date: Tuesday, June 21
            </div>

            <div class="cart-item-details-grid">
              <img class="product-image"
                src=${matchingProduct.image}>

              <div class="cart-item-details">
                <div class="product-name">
                  ${matchingProduct.name}
                </div>
                <div class="product-price">
                  $${formatCurrency(matchingProduct.priceCents)}
                </div>
                <div class="product-quantity">
                  <span>
                    Quantity: <span class="quantity-label">${value.quantity}</span>
                  </span>
                  <span class="update-quantity-link link-primary js-update-link">
                    Update
                  </span>
                  <span class="delete-quantity-link link-primary js-delete-link" 
                  data-product-id = "${matchingProduct.id}">
                    
                  Delete
                  </span>
                </div>
              </div>

              <div class="delivery-options">
                <div class="delivery-options-title">
                  Choose a delivery option:
                </div>
                <div class="delivery-option">
                  <input type="radio" checked
                    class="delivery-option-input"
                    name="delivery-option-${matchingProduct.id}">
                  <div>
                    <div class="delivery-option-date">
                      Tuesday, June 21
                    </div>
                    <div class="delivery-option-price">
                      FREE Shipping
                    </div>
                  </div>
                </div>
                <div class="delivery-option">
                  <input type="radio"
                    class="delivery-option-input"
                    name="delivery-option-${matchingProduct.id}">
                  <div>
                    <div class="delivery-option-date">
                      Wednesday, June 15
                    </div>
                    <div class="delivery-option-price">
                      $4.99 - Shipping
                    </div>
                  </div>
                </div>
                <div class="delivery-option">
                  <input type="radio"
                    class="delivery-option-input"
                    name="delivery-option-${matchingProduct.id}">
                  <div>
                    <div class="delivery-option-date">
                      Monday, June 13
                    </div>
                    <div class="delivery-option-price">
                      $9.99 - Shipping
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          `;
    checkout+=html1;
});        

    document.querySelector(".js-order-summary").innerHTML = checkout;

    document.querySelectorAll(".js-delete-link").forEach((link)=>{ //Here to practise try to het the id of the 
        link.addEventListener("click", ()=> {                      //product whose delete button got clicked
        const productID = link.dataset.productId;
        removeFromCart(productID);     
        document.querySelector(`.js-cart-item-container-${productID}`).remove();
        /* console.log(container); */
        updateCartQuantity();
        
        })
    });

  function updateCartQuantity(){
  let cartQuantity =0;

    cart.forEach((value)=>{
      cartQuantity+=value.quantity;
      })
  /* document.querySelector(".js-cart-quantity").innerHTML = cartQuantity; */
  document.querySelector(".noOfItems").innerHTML=cartQuantity; 
}
updateCartQuantity();

    