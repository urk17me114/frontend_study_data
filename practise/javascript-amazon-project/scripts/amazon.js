
  import {cart} from "../data/cart.js"
  import {products} from "../data/products.js"
        
        //Save the data
/* const products = [
    {   image:"images/products/athletic-cotton-socks-6-pairs.jpg",
        name:  "Black and Gray Athletic Cotton Socks - 6 Pairs",
        priceCents:1090,
        quantity:1,
        rating:{stars:4.5,
                count:87}
    },
    {   image:"images/products/intermediate-composite-basketball.jpg",
        name:  "Intermediate Size Basketball",
        priceCents:2095,
        quantity:1,
        rating:{stars:4,
                count:127}
    },
    {
        image:"images/products/adults-plain-cotton-tshirt-2-pack-teal.jpg",
        name:  "Adults Plain Cotton T-Shirt - 2 Pack",
        priceCents:799,
        quantity:1,
        rating:{stars:4.5,
                count:56}
    }
];  */

    //Generate the HTML
    
    let productsHTML = "";
    products.forEach((value,index)=>{
        const html = `
        <div class="product-container">
          <div class="product-image-container">
            <img class="product-image"
              src="${value.image}">
          </div>

          <div class="product-name limit-text-to-2-lines">
            ${value.name}
          </div>

          <div class="product-rating-container">
            <img class="product-rating-stars"
              src="images/ratings/rating-${(value.rating.stars)*10}.png">
            <div class="product-rating-count link-primary">
              ${value.rating.count}
            </div>
          </div>

          <div class="product-price">
            $${(value.priceCents/100).toFixed(2)}
          </div>

          <div class="product-quantity-container">
            <select>
              <option selected value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
            </select>
          </div>

          <div class="product-spacer"></div>

          <div class="added-to-cart">
            <img src="images/icons/checkmark.png">
            Added
          </div>

          <button class="add-to-cart-button button-primary js-add-to-cart"
          data-product-id = "${value.id}"
          data-product-name = "${value.name}">
            Add to Cart
          </button>
        </div>`;
    productsHTML+=html;
    }
        
);

/* data attribute is an HTML attribute which uses kebab-case. syntax is always it should start with 
  data-any-name = ${value.parameter} */

//put it on the webpage using DOM
document.querySelector(".js-products-grid").innerHTML=productsHTML;
document.querySelectorAll(".js-add-to-cart").forEach((button)=>{
  button.addEventListener("click",()=>{
      quantityCheck(button);
})});
    
function quantityCheck(button){
  alert("Added to cart");
      const productID = button.dataset.productId; /* kebab case gets changed to camelCase (produt-id to productId)*/
      const productName = button.dataset.productName; 
      
      /* Logic : Check the cart → if item exists, increase quantity in cart → otherwise add it in matchingItem.” */
      let matchingItem;
      
      if (cart.forEach((value)=>{
        if (productID===value.id){
          matchingItem=value;

        }
  }));
      
      if(matchingItem){
          matchingItem.quantity+=1;
      }
      else{
        cart.push({
          id: productID,
          name:productName,
          quantity:1
        });
      }

      let cartQuantity =0;

      cart.forEach((value)=>{
        cartQuantity+=value.quantity;
        })
    document.querySelector(".js-cart-quantity").innerHTML = cartQuantity;
    console.log(cart);
}
    





    
