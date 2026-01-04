import {renderOrderSummary} from "../scripts/checkout/orderSummary.js";
import {renderPaymentSummary} from "../scripts/checkout/paymentSummary.js";
/* import "../data/backend-practice.js"; */
import { loadProducts } from "../data/products.js"; 


document.addEventListener("DOMContentLoaded", () => {
  loadProducts(()=> //format of a callback function
    {renderOrderSummary();
      renderPaymentSummary();
    });
  
  
});



