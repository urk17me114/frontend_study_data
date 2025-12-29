import {cart,removeFromCart,updateDeliveryOption} from "../../data/cart.js"
import { products } from "../../data/products.js";
import { formatCurrency} from "../utils/money.js";
/* for dayjs the syntax is different as it is export default dayjs() in the ext file */
import dayjs from "https://unpkg.com/supersimpledev@8.5.0/dayjs/esm/index.js" 
import {deliveryOptions} from "../../data/deliveryOptions.js";
import { renderPaymentSummary } from "./paymentSummary.js";


/* esm vertion of external library means using an export tag. when esm is not there in 
ext library we cant use as modules so script tags has to be used */



export function renderOrderSummary(){
  let checkout = "";
  cart.forEach((value)=>{
      const productID = value.id;
      
      let matchingProduct;   //if the productID in cart matches with the id of products then store all the respective
      products.forEach((product)=>{   //details into a reference called matchingProduct
          if (product.id ===  productID){
              matchingProduct=product;
          }
      });

      const deliveryOptionId = value.deliveryOptionId;
      let deliveryOption;
      deliveryOptions.forEach((option)=>{
        if(option.id === deliveryOptionId){
          deliveryOption=option;
        }
      });

      
      const today = dayjs();
      const deliveryDate = today.add(deliveryOption.deliveryDays,"days");
      const dateString = (deliveryDate.format('dddd MMMM D'));
    
      
      const html1 = 
          `<div class="cart-item-container js-cart-item-container-${matchingProduct.id}">
              <div class="delivery-date">
                Delivery date: ${dateString}
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
                  <div class="product-quantity js-product-quantity-${matchingProduct.id}">
                    <span>
                      Quantity: <span class="quantity-label">${value.quantity}</span>
                    </span>
                    <span class="update-quantity-link link-primary js-update-link">
                      Update
                    </span>
                    <span class="delete-quantity-link link-primary js-delete-link js-delete-link-${matchingProduct.id}" 
                    data-product-id = "${matchingProduct.id}">
                      
                    Delete
                    </span>
                  </div>
                </div>

                <div class="delivery-options">
                  <div class="delivery-options-title">
                    Choose a delivery option:
                  ${deliveryOptionsHTML(matchingProduct,value)}
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
          renderPaymentSummary();
          
          })
      });

    
    
      function deliveryOptionsHTML(matchingProduct,value){
        let html="";
      deliveryOptions.forEach((deliveryOption)=>{
        const today = dayjs();
        const deliveryDate = today.add(deliveryOption.deliveryDays,"days");
        const dateString = (deliveryDate.format('dddd MMMM D'));
        const priceString = deliveryOption.priceCents===0 ? 'FREE'
          : `$${formatCurrency(deliveryOption.priceCents)}`;
        const isChecked = deliveryOption.id  === value.deliveryOptionId;
                
        html+= `<div class="delivery-option js-delivery-option" 
                data-product-id="${matchingProduct.id}"
                data-delivery-option-id = "${deliveryOption.id}">
                    <input type="radio"
                      ${isChecked? 'checked':''}
                      class="delivery-option-input"
                      name="delivery-option-${matchingProduct.id}">
                    <div>
                      <div class="delivery-option-date">
                        ${dateString}
                      </div>
                      <div class="delivery-option-price">
                        ${priceString} - Shipping
                      </div>
                    </div>
                  </div>`
                            
      });
      return html;
    }

    function updateCartQuantity(){
    let cartQuantity =0;

      cart.forEach((value)=>{
        cartQuantity+=value.quantity;
        })
    /* document.querySelector(".js-cart-quantity").innerHTML = cartQuantity; */
    document.querySelector(".noOfItems").innerHTML=cartQuantity; 
  }
  updateCartQuantity();


  document.querySelectorAll(".js-delivery-option").forEach((element)=>{
    element.addEventListener("click",()=>{
      const {productId,deliveryOptionId} = element.dataset; 
      updateDeliveryOption(productId,deliveryOptionId);
      renderOrderSummary(); //calling a function inside a fn called recursion
      renderPaymentSummary();
    });});
  }
  


    