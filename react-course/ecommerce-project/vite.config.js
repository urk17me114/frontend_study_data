import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: { //This is called a server proxy relationship
    proxy:{
      '/api':{
        target: 'http://localhost:3000' /* This means that if the url path starts with /api it the request will automatically 
                                        go into localhost 3000 */
      },
      '/images':{
        target : 'http://localhost:3000' /* Also in index .html update <base href="/"/> */
      }
      
    }
  }
})
