
/* Use PascalCase for things that generate objects */

class Cart{
     cartItems ;
     localStorageKey ;

     constructor(localStorageKey){
        /* property = parameter */
        this.localStorageKey = localStorageKey;
        this.loadFromStorage();
        
     }
    
     loadFromStorage(){
      this.cartItems = JSON.parse(localStorage.getItem(this.localStorageKey)); /* To convert string to array */
    
      if(!this.cartItems){
      this.cartItems = [
        
      {
        id: "e43638ce-6aa0-4b85-b27f-e1d07eb678c6",
        name: "Black and Gray Athletic Cotton Socks - 6 Pairs",
        quantity:1,
        deliveryOptionId: "1"
        },
        {
        id: "3ebe75dc-64d2-4137-8860-1f5a963e534b",
        name: "6 Piece White Dinner Plate Set",
        quantity:1,
        deliveryOptionId: "2"
      }];
    
      this.saveToStorage();
    }

      
    };

    saveToStorage(){
        localStorage.setItem(this.localStorageKey,JSON.stringify(this.cartItems));
    };

    addToCart(productID,productName){
  /* Logic : Check the cart → if item exists, increase quantity in cart → otherwise add it in matchingItem.” */

            let matchingItem;
                
                this.cartItems.forEach((value)=>{
                if (productID===value.id){
                    matchingItem=value;

                }
            });
                
                if(matchingItem){
                    matchingItem.quantity+=1;
                }
                else{
                this.cartItems.push({
                    id: productID,
                    name:productName, 
                    quantity:1,
                    deliveryOptionId: "1"
                });
                }
                this.saveToStorage();
            };



    removeFromCart(product_id){
            const newCart = [];
            this.cartItems.forEach((value)=>{
                if(value.id!==product_id){
                newCart.push(value); 
                }
            })
            this.cartItems = newCart;
            this.saveToStorage();
            };

    updateDeliveryOption(productID,deliveryOptionId){
            let matchingItem;
            this.cartItems.forEach((value)=>{
                if (productID===value.id){
                    matchingItem=value;

                }
            });
            
            matchingItem.deliveryOptionId=deliveryOptionId;
            this.saveToStorage();
            };

}



//Here all the code below is called the setup code
//A constructor let  us put this setup code inside the class

/* const object = new Class */
const cart = new Cart("cart-OOP");
const businessCart = new Cart("businessCart");



cart.addToCart("77919bbe-0e56-475b-adde-4f24dfed3a04");

console.log(cart);
console.log(businessCart);

















