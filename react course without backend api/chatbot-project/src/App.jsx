import './App.css'
import { ChatInput } from './components/ChatInput.jsx'
import  ChatMessages  from './components/ChatMessages.jsx'
import { useState } from 'react'

    
    

function App(){

            const [chatMessage,setChatMessage] =  useState([/* { //This returns an array 
                    message:"Hi",
                    imgsrc:"user",
                    id: "id1"
                },
                {
                    message:"How can I help you",
                    imgsrc:"robot",
                    id: "id2"
            },{
                    message:"I am fine.. Whats the weather today",
                    imgsrc:"user",
                    id: "id3"
                },
                {
                    message:"It is sunny",
                    imgsrc:"robot",
                    id: "id4"
            } */]);
             
                return( <div className = "app-container">
                        <ChatMessages className = "ChatMessages" chatMessage = {chatMessage}/>
                        <ChatInput 
                            chatMessage = {chatMessage}
                            setChatMessage = {setChatMessage}></ChatInput>
                    </div>)
    }/* creating our own html element */
export default App
