import {cart} from "../../data/cart.js";
import { getProduct } from "../../data/products.js";
import { getDeliveryOption } from "../../data/deliveryOptions.js";
import { formatCurrency } from "../../scripts/utils/money.js"; 


export function renderPaymentSummary(){
    
    const container = document.querySelector(".js-payment-summary");
    if (!container) return;  // <-- prevent TypeError in tests
    let productPriceCents = 0;
    let shippingPriceCents = 0;
    let totalBeforeTax = 0;
    cart.forEach((cartItem)=>{
        const product = getProduct(cartItem.id);
        productPriceCents+=cartItem.quantity*product.priceCents;
        const deliveryOPtion = getDeliveryOption(cartItem.deliveryOptionId);
        shippingPriceCents+=deliveryOPtion.priceCents;
        
    })
    totalBeforeTax += shippingPriceCents+productPriceCents;
    const estimaedTax = (totalBeforeTax*0.1);
    const totalCents = totalBeforeTax + estimaedTax;
    console.log(productPriceCents);
    console.log(shippingPriceCents);
    console.log(totalBeforeTax);
    console.log(estimaedTax);
    console.log(totalCents);
    const paymentSummaryHTML = 
    `<div class="payment-summary-title">
    Order Summary
    </div>

    <div class="payment-summary-row">
    <div>Items (${cart.length}):</div>
    <div class="payment-summary-money">$${formatCurrency(productPriceCents)}</div>
    </div>

    <div class="payment-summary-row">
    <div>Shipping &amp; handling:</div>
    <div class="payment-summary-money">$${formatCurrency(shippingPriceCents)}</div>
    </div>

    <div class="payment-summary-row subtotal-row">
    <div>Total before tax:</div>
    <div class="payment-summary-money">$${formatCurrency(totalBeforeTax)}</div>
    </div>

    <div class="payment-summary-row">
    <div>Estimated tax (10%):</div>
    <div class="payment-summary-money">$${formatCurrency(estimaedTax)}</div>
    </div>

    <div class="payment-summary-row total-row">
    <div>Order total:</div>
    <div class="payment-summary-money">$${formatCurrency(totalCents)}</div>
    </div>

    <button class="place-order-button button-primary">
    Place your order
    </button>
    `

    container.innerHTML=paymentSummaryHTML;
    console.log("Cart contents:", cart);


}

