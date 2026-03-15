    export function cartQuantity(cart){
        let totalQuantity = 0;
        
        cart.forEach((cartItem) => {
            totalQuantity += cartItem.quantity 
        })
        return(totalQuantity);
    }