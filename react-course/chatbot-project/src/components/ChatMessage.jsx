import robot from '../assets/images/robot_img.png'
import user from '../assets/images/user_img.png'

export function ChatMessage({message,imgsrc}){
            
          
             return(<div className = {imgsrc==="user" ? "chat-message-user":"chat-message-robot" }>   
                        {imgsrc === "robot" && <img src= {robot} width = "30" ></img>}
                        <div className = "chat-message">{message}</div> 
                        {imgsrc === "user" && <img src= {user} width = "30" ></img>}
                        
                    </div>);
    } 