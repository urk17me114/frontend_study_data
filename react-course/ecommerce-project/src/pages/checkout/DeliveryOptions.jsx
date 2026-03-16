import dayjs from "dayjs"
import { Money } from "../../assets/utils/money"

export function DeliveryOptions({deliveryOptions,cartItem}){
    return(
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
    )
}