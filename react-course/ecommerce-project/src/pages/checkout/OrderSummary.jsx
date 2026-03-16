import dayjs from 'dayjs'
import { Money } from '../../assets/utils/money'
import { DeliveryOptions } from './DeliveryOptions'

export function OrderSummary({cart,deliveryOptions}){
    return(
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
        
                            <DeliveryOptions deliveryOptions={deliveryOptions} cartItem={cartItem} />
                            
                            </div>
                        </div>)
                        })}
                        
        
                        
                        </div>
    )
}