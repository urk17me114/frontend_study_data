
//Integration Tests
import {renderOrderSummary} from "../../scripts/checkout/orderSummary.js";
import {loadFromStorage} from "../../data/cart.js";

describe("TestSuite: OrderSummary",()=>{
    it("displays the cart",()=>{
        document.querySelector(".js-test-container").innerHTML=`
        <div class="js-order-summary"></div>
        <div class="noOfItems"></div>`;
    

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
            

            expect(
                document.querySelectorAll(".cart-item-container").length).toEqual(2);
            
                expect(
                document.querySelector(`.js-product-quantity-${"e43638ce-6aa0-4b85-b27f-e1d07eb678c6"}`).innerText).toContain("Quantity: 1");
            

        });
        });
