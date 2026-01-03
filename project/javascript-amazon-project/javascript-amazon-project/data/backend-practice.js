/* HTTP stands for HyperText Transfer Protocal */

const xhr = new XMLHttpRequest();

 xhr.addEventListener("load",()=>{
    console.log(xhr.response);
})


xhr.open("GET","https://supersimplebackend.dev/products/first") //it prepares the request
xhr.send(); // this sends the request

//syntax is first parameter what type of request and second where to send this request
//Types of requests are get,post,put,delete

console.log(xhr.response);//nothing will appear as this loc runs before getting the response
