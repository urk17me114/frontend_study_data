import {cart} from "../../data/cart.js";
import { getProduct } from "../../data/products.js";
import { getDeliveryOption } from "../../data/deliveryOptions.js";
import { formatCurrency } from "../../scripts/utils/money.js"; 
import {addOrder} from "../../data/orders.js"


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

    <button class="place-order-button button-primary js-place-order">
    Place your order
    </button>
    `

    container.innerHTML=paymentSummaryHTML;
    console.log("Cart contents:", cart);

    /* There are 4 types of requests
    GET: get something from the backend
    POST: create something
    PUT: update something
    DELETE: delete something
     */
    
    document.querySelector(".js-place-order").addEventListener("click", async () => {
    const button = document.querySelector(".js-place-order");
      
        /* button.disabled = true;

        if (!cart || !Array.isArray(cart) || cart.length === 0) {
            alert("Your cart is empty!");
            return;
        } */

        const payload = {
            cart: cart.map(item => ({//as per the backend it is productId and not id
                productId: item.id,
                quantity: item.quantity,
                deliveryOptionId: item.deliveryOptionId
            }))
        };

        const response = await fetch("https://supersimplebackend.dev/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

       /*  if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server error ${response.status}: ${errText}`);
        } */

        const order = await response.json();
        console.log("Order successful:", order);
         addOrder(order);
        /* // ✅ Clear cart safely
        cart.length = 0;              // clear array without reassigning
        localStorage.removeItem("key"); */
/*
    } catch (err) {
        console.error("Failed to place order:", err);
        alert("Failed to place order. Check console for details.");
    } finally {
        button.disabled = false;
    } */

        window.location.href = "orders.html"; //this will replace everything after 127.0.0.1:5500/ from checkout.html to orders.html
});





}

