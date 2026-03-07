import { useRef,useEffect } from 'react'
import {ChatMessage} from './ChatMessage.jsx'

 function ChatMessages({chatMessage}){ 
        
       /*  ref is a container with special react features. It can save a HTML element from the component inside the ref container */
        const chatMessagesRef =  useRef(null);     


        /* useEffect lets us run some code after the component is created or updated */
            useEffect(()=>{const containerElem = chatMessagesRef.current
                                     if(containerElem){
                containerElem.scrollTop = containerElem.scrollHeight; }
            },[chatMessage]);
           
            
                 /* here the array controls when the useEffect is to be executed */
            
            return ( <div className = "chat-message-container" 
                        ref = {chatMessagesRef}>

                        {chatMessage.length === 0 && (
                        <div style={{ textAlign: "center", marginTop: "20px", color: "#666" }}>
                        Welcome to the chatbot project! Send a message using the textbox below.
                        </div>
                    )}
                
                {chatMessage.map((chatMessage)=>{return (<ChatMessage        message = {chatMessage.message} 
                                                                            imgsrc = {chatMessage.imgsrc}
                                                                            key = {chatMessage.id}/>
                                                        );} ) }</div>) 
    }

    export default ChatMessages;