import {renderOrderSummary} from "../scripts/checkout/orderSummary.js";
import {renderPaymentSummary} from "../scripts/checkout/paymentSummary.js";



document.addEventListener("DOMContentLoaded", () => {
  renderOrderSummary();
  renderPaymentSummary();
});