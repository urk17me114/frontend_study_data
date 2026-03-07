import {Chatbot} from 'supersimpledev' //if from is not given it is understood to be taken from node_modules folder
import { useState } from 'react'


export function ChatInput({chatMessage,setChatMessage}){ 
            const [inputText,setInputText]=useState("") 
            
            function saveInputText(event){ 
              setInputText(event.target.value)//here its different as it is a string 

            }

            function sendMessage(){
                
                const response = Chatbot.getResponse(inputText);
                setChatMessage([...chatMessage,{
                            message: inputText,
                            imgsrc: "user",
                            id:crypto.randomUUID()
                        },{
                            message: response,
                            imgsrc: "robot",
                            id:crypto.randomUUID()
                        } //this takes the value in this array(old array) and copies them to new array setChatMessages
                    ]);
                    
                    
                    //console.log(response);
                    setInputText("");
            }
            
                return( /* Here value is called a controlled input */
                <div className = "chat-input-container">    
                    <input className = "chat-input" placeholder = "Send a message to chatbot" onChange = {saveInputText} value={inputText}></input>
                    <button onClick = {sendMessage} className = "send-button">Send</button>
                </div>
                );
                
    } 