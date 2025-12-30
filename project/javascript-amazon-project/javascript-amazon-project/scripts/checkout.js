import {renderOrderSummary} from "../scripts/checkout/orderSummary.js";
import {renderPaymentSummary} from "../scripts/checkout/paymentSummary.js";
import "../data/cart-class.js"


document.addEventListener("DOMContentLoaded", () => {
  renderOrderSummary();
  renderPaymentSummary();
});