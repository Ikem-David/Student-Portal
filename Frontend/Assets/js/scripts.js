const API_URL = "http://localhost:8000"

document.getElementById("loginForm").addEventListener("submit", async function(e){
    
    const username = document.getElementById("Email")
    const password = document.getElementById("Password") 
try {
    
    let response =await fetch(`${API_URL}/auth/login`, {
        method:"POST",
        body:{
            username, password
        }
    })
    if(response.ok){
        const data = await response.json()
        console.log(data)
    }
} catch (error) {
    console.log(error)
}
})
   