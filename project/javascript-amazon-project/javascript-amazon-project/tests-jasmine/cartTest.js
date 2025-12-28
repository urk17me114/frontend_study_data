import {addToCart,cart,loadFromStorage} from "../data/cart.js";


describe("Testsuite: Add to Cart",()=>{
    
   
    it("adds a new product to the cart",()=>{
        spyOn(localStorage,"getItem").and.callFake(()=>{
            return JSON.stringify([]);
        });
        loadFromStorage();
        
        //This will replace the localstorage method getItem with a fake version
        //by using this we replaced the getItem in local storage to an empty array
        addToCart("e43638ce-6aa0-4b85-b27f-e1d07eb678c6");
        expect(cart.length).toEqual(1);
        expect(cart[0].id).toEqual("e43638ce-6aa0-4b85-b27f-e1d07eb678c6");
        expect(cart[0].quantity).toEqual(1);

              
    });
    
    it("adds an existing product to the cart",()=>{
        spyOn(localStorage,"getItem").and.callFake(()=>{
            return JSON.stringify([{id: "e43638ce-6aa0-4b85-b27f-e1d07eb678c6",
                                    name: "Black and Gray Athletic Cotton Socks - 6 Pairs",
                                    quantity:1,
                                    deliveryOptionId: "1"}]);

        });
        loadFromStorage();
        
        //This will replace the localstorage method getItem with a fake version
        //by using this we replaced the getItem in local storage to an empty array
        addToCart("e43638ce-6aa0-4b85-b27f-e1d07eb678c6");
        expect(cart.length).toEqual(1);
        expect(cart[0].id).toEqual("e43638ce-6aa0-4b85-b27f-e1d07eb678c6");
        expect(cart[0].quantity).toEqual(2);

});
});