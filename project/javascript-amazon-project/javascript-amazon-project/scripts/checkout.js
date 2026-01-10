import {renderOrderSummary} from "../scripts/checkout/orderSummary.js";
import {renderPaymentSummary} from "../scripts/checkout/paymentSummary.js";
/* import "../data/backend-practice.js"; */
import { loadProducts,loadProductsFetch } from "../data/products.js"; //loadProductsFetch to be imported
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


      
      
      
      
      
      
     /*  //promise.all helps to run an array of functions parallely without waiting for one to finish
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
      
    }); */


   /*  Promise.all([ //using loadProductsFetch
      loadProductsFetch(),
      new Promise((resolve)=>{
        loadCart(()=>{
        resolve();
      });})
    ]).then(()=>{
      renderOrderSummary();
      renderPaymentSummary();
      
    }); */
      
 
 
 
 
    
    //asyncawait  await let us write asynchronous code like normal code
      async function loadPage(){ //async makes a function return a promise 
        try{
          //throw "error1" // behaves like all the loc inside tryblock is commented
        await loadProductsFetch(); //syntax when not using a callback function       
        
        await new Promise((resolve)=>{
          loadCart(()=>{
            resolve(); //here the value of a is passed onto b using resolve
          });
        })
          renderOrderSummary();
          renderPaymentSummary(); 
      } catch(error){ //try catch syntax when the first fn is a fetch fn
          console.log("errrrr");
          console.log(error);//the value error1 is stored in error
        }
        //console.log(b);

        }
        loadPage();







        /* 
        //To be figured out later as it is not working
        //try catch syntax is different when a call back is used
      async function loadPage(){ //async makes a function return a promise
       const a = await new Promise((resolve)=>{ //syntax when using a callback function
          loadProducts(()=>{
            try{
            resolve("value 6")
          }
         catch(error)  { // error callback
        console.log("errrrrrrrr");
          };
        })});
        console.log(a);
        
        const b = await new Promise((resolve)=>{
          loadCart(()=>{
            resolve(a); //here the value of a is passed onto b using resolve
          });
        })
          
          renderOrderSummary();
          renderPaymentSummary(); 
          console.log(b);
      } 


        
              loadPage(); */
 
 
  });


  
  
  
  
  
  
  
  
  
  
  
  
  /* //we cant use await inside a normal function
    async function outerFunction(){
      console.log("hello");
    
      function cannotBeDone(){
      await loadProductsFetch(); //we cant use await inside a normal function
    }} */


