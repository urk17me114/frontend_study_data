
import './checkout-header.css'
import './checkout.css'
import {Money}   from '../assets/utils/money'
import { cartQuantity } from '../assets/utils/cartQuantity';
import axios from 'axios';
import { useEffect,useState } from 'react';
import dayjs from 'dayjs'


export function Checkout({cart}){
const totalQuantity = cartQuantity(cart);

const [deliveryOptions,setDeliveryOptions] = useState([])
const [paymentSummary,setPaymentSummary] = useState([]) /* payment summary is an object and it is much easy to check 
                                                             if the object is null loaded if we set it to null at the start */
useEffect(()=>{
    axios.get('/api/delivery-options?expand=estimatedDeliveryTime').then((response)=>{
      setDeliveryOptions(response.data) 
      
    }),axios.get('/api/payment-summary').then((response)=>{
      setPaymentSummary(response.data) 
      console.log(response.data)
    })
},[])
return(
        <>
        <title>Checkout</title>
            

            <div className="checkout-header">
            <div className="header-content">
                <div className="checkout-header-left-section">
                <a href="/">
                    <img className="logo" src="images/logo.png" />
                    <img className="mobile-logo" src="images/mobile-logo.png" />
                </a>
                </div>

                <div className="checkout-header-middle-section">
                Checkout (<a className="return-to-home-link"
                    href="/">{totalQuantity} items</a>)
                </div>

                <div className="checkout-header-right-section">
                <img src="images/icons/checkout-lock-icon.png" />
                </div>
            </div>
            </div>

            <div className="checkout-page">
            <div className="page-title">Review your order</div>

            <div className="checkout-grid">
                <div className="order-summary">
                {deliveryOptions.length>0 && cart.map((cartItem)=>{ /* The deliveryoptions start as empty as defined in useState. 
                                            If its empty we maynot find the selectedDeliveryOption. 
                                            To fix this we check deliveryOptions.length>0 */
                    const selectedDeliveryOption = deliveryOptions.find((deliveryOption)=>{
                            return deliveryOption.id === cartItem.deliveryOptionId
                    })
                    return(<div key = {cartItem.productId} className="cart-item-container">
                    <div className="delivery-date">
                    {`Delivery date: ${dayjs(selectedDeliveryOption.estimatedDeliveryTimeMs).format("dddd, MMMM, D")}`}
                    {/* {console.log(selectedDeliveryOption)} */}
                    </div>

                    <div className="cart-item-details-grid">
                    <img className="product-image"
                        src={cartItem.product.image} />

                    <div className="cart-item-details">
                        <div className="product-name">
                        {cartItem.product.name}
                        </div>
                        <div className="product-price">
                        ${Money(cartItem.product.priceCents)}
                        </div>
                        <div className="product-quantity">
                        <span>
                            Quantity: <span className="quantity-label">{cartItem.quantity}</span>
                        </span>
                        <span className="update-quantity-link link-primary">
                            Update
                        </span>
                        <span className="delete-quantity-link link-primary">
                            Delete
                        </span>
                        </div>
                    </div>

                    <div className="delivery-options">
                        <div className="delivery-options-title">
                        Choose a delivery option:
                        </div>
                        {deliveryOptions.map((deliveryOption)=>{
                            let priceString = "Free Shipping"
                            if(deliveryOption.priceCents>0){
                                priceString = `${Money(deliveryOption.priceCents)} - shipping`
                            }
                            return(
                                 <div key={deliveryOption.id} className="delivery-option">
                                <input type="radio" checked = {deliveryOption.id===cartItem.deliveryOptionId}
                                    className="delivery-option-input"
                                    name={`delivery-option-${cartItem.productId}`} /> {/* The name groups radio buttons together.
                                                                All radio buttons with the same name belong to the same group, 
                                                                meaning only one can be selected. Therefore we change the name 
                                                                which is currently delivery-option-1 for all the products
                                                                to delivery-option-productid */}
                                    
                                <div>
                                    <div className="delivery-option-date">
                                    {dayjs(deliveryOption.estimatedDeliveryTimeMs).format("dddd, MMMM, D")} {/* To give the particular estimated time in a particular format */}
                                    </div>
                                    <div className="delivery-option-price">
                                    {priceString}
                                    </div>
                                </div>
                                </div>
                            )
                        })}
                       
                       
                    </div>
                    </div>
                </div>)
                })}
                

                
                </div>

                <div className="payment-summary">
                    <div className="payment-summary-title">
                    Payment Summary
                    </div>
                    {paymentSummary && (<>
                    <div className="payment-summary-row">
                    <div>Items ({paymentSummary.totalItems}):</div>
                    <div className="payment-summary-money">{`$${Money(paymentSummary.productCostCents)}`}</div>
                    </div>

                    <div className="payment-summary-row">
                    <div>Shipping &amp; handling:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.shippingCostCents)}</div>
                    </div>

                    <div className="payment-summary-row subtotal-row">
                    <div>Total before tax:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostBeforeTaxCents)}</div>
                    </div>

                    <div className="payment-summary-row">
                    <div>Estimated tax (10%):</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostBeforeTaxCents/10)}</div>
                    </div>

                    <div className="payment-summary-row total-row">
                    <div>Order total:</div>
                    <div className="payment-summary-money">${Money(paymentSummary.totalCostCents)}</div>
                    </div>

                    <button className="place-order-button button-primary">
                    Place your order
                    </button></>)}
                </div>
            </div>
            </div>
        
</>)}