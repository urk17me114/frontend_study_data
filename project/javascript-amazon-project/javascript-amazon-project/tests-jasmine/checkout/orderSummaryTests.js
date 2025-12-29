
//Integration Tests
import {renderOrderSummary} from "../../scripts/checkout/orderSummary.js";
import {loadFromStorage,cart} from "../../data/cart.js";

describe("TestSuite: OrderSummary",()=>{
    
    beforeEach(()=>{
        document.querySelector(".js-test-container").innerHTML=`
        <div class="js-order-summary"></div>
        <div class="noOfItems"></div>
        <div class="js-payment-summary"></div>`;
    

    spyOn(localStorage,"getItem").and.callFake(()=>{
                return JSON.stringify([{
                                            id: "e43638ce-6aa0-4b85-b27f-e1d07eb678c6",
                                            name: "Black and Gray Athletic Cotton Socks - 6 Pairs",
                                            quantity:1,
                                            deliveryOptionId: "1"
                                            },
                                            {
                                            id: "3ebe75dc-64d2-4137-8860-1f5a963e534b",
                                            name: "6 Piece White Dinner Plate Set",
                                            quantity:4,
                                            deliveryOptionId: "2"
                                        }]);
                                    });
            loadFromStorage();
            renderOrderSummary();
    });
    
    it("displays the cart",()=>{
    
            expect(
                document.querySelectorAll(".cart-item-container").length).toEqual(2);
            
                expect(
                document.querySelector(`.js-product-quantity-${"e43638ce-6aa0-4b85-b27f-e1d07eb678c6"}`).innerText).toContain("Quantity: 1");
            

        });

    it("remove a product",()=>{
                document.querySelector(`.js-delete-link-${"3ebe75dc-64d2-4137-8860-1f5a963e534b"}`).click();
                expect(
                
                document.querySelectorAll(".cart-item-container").length).toEqual(1);
                
                
                expect(
                document.querySelector(`.js-cart-item-container-${"3ebe75dc-64d2-4137-8860-1f5a963e534b"}`)).toBeNull();
        
                expect(
                document.querySelector(`.js-cart-item-container-${"e43638ce-6aa0-4b85-b27f-e1d07eb678c6"}`)).not.toBeNull();
                
                expect(
                cart.length).toEqual(1);

                expect(cart[0].id).toEqual("e43638ce-6aa0-4b85-b27f-e1d07eb678c6")
        
            })
                

        });
