import {renderOrderSummary} from "../scripts/checkout/orderSummary.js";
import {renderPaymentSummary} from "../scripts/checkout/paymentSummary.js";
/* import "../data/backend-practice.js"; */
import { loadProducts } from "../data/products.js"; 
import { loadCart } from "../data/cart.js"; 


document.addEventListener("DOMContentLoaded", () => {
  /* loadProducts(()=> //format of a callback function
    {renderOrderSummary();
      renderPaymentSummary();
    }); */


    /* new Promise((resolve)=>{  //alt way of using callback fns using promise
      loadProducts(()=>{ //inorder to call resolve the fn used should be a callback function
        resolve("value1");
      });
    }).then((value)=>{ //the value stored in the above resolve will be passed on to the value in the next step then
      return new Promise((resolve)=>{
        loadCart(()=>{
        console.log(value);
        resolve();
      });});})
      .then(()=>{
        renderOrderSummary();
        renderPaymentSummary();
      }); */


      //promise.all helps to run an array of functions parallely without waiting for one to finish
    Promise.all([
      new Promise((resolve)=>{  //alt way of using callback fns using promise
      loadProducts(()=>{ //inorder to call resolve the fn used should be a callback function
        resolve();
      });
    }),
      new Promise((resolve)=>{
        loadCart(()=>{
        resolve();
      });})
    ]).then(()=>{
      renderOrderSummary();
      renderPaymentSummary();
    });
      
  });


