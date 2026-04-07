<script>
  let email = "";
  let password = "";
  let showPassword = false; 

  async function login(event) {
    event.preventDefault();
    const usuario = { email, password };

    try {
      const response = await fetch("https://fastapi1-3jjn.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(usuario)
      });

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        showNotification("✅ Login exitoso", "success");
        setTimeout(() => window.location.href = "/search_student", 500);
      } else {
        showNotification(data.detail || "❌ Credenciales inválidas", "error");
      }
    } catch (error) {
      console.error(error);
    }
  }

  function showNotification(message, type) {
    const notif = document.getElementById("notification");
    notif.textContent = message;
    notif.className = "notification show " + type;
    setTimeout(() => notif.classList.remove("show"), 1000);
  }

  function togglePassword() {
    showPassword = !showPassword;
  }
</script>

<head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<div class="container">
  <h1>Bienvenido a la página</h1>

  <form on:submit={login}>
    <div>
      <label>Email
        <input type="text" bind:value={email} required>
      </label>
    </div>

    <div class="password-wrapper">
      <!-- svelte-ignore a11y_label_has_associated_control -->
      <label>Password</label>
      <input type={showPassword ? "text" : "password"} bind:value={password} required>
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <span class="toggle-password" on:click={togglePassword}>
            <span class="material-icons">
                {showPassword ? "visibility_off" : "visibility"}
            </span>
        </span>

    </div>

    <button type="submit">Iniciar sesión</button>

    <a class="register-link" href="/register">
      ¿No tienes una cuenta? Regístrate aquí
    </a>
  </form>
</div>
<div id="notification" class="notification"></div>

<style>

:global(body){
    background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:"Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.container{
    max-width:420px;
    width:100%;
    padding:40px;
    border-radius:20px;
    background:rgba(255,255,255,0.25);
    box-shadow:0 8px 32px rgba(0,0,0,0.15);
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.18);
}

h1{
    text-align:center;
    margin-bottom:25px;
    color:#1a237e;
    font-weight:700;
}

form{
    display:flex;
    flex-direction:column;
}

label{
    font-size:14px;
    font-weight:600;
    color:#1a237e;
    margin-bottom:6px;
}

input{
    width:100%;
    padding:12px;
    border-radius:10px;
    border:1px solid #cfd8dc;
    font-size:14px;
    transition:all 0.3s ease;
    background:rgba(255,255,255,0.8);
}

input:focus{
    outline:none;
    border-color:#1976d2;
    box-shadow:0 0 0 3px rgba(25,118,210,0.2);
}

button{
    margin-top:15px;
    padding:14px;
    background:#1976d2;
    color:white;
    border:none;
    border-radius:10px;
    font-size:15px;
    font-weight:600;
    cursor:pointer;
    transition:transform 0.2s ease, background 0.3s ease;
}

button:hover{
    background:#1565c0;
    transform:scale(1.02);
}

button:active{
    transform:scale(0.98);
}

.register-link{
    display:block;
    text-align:center;
    font-size:14px;
    color:#1976d2;
    text-decoration:none;
    margin-top:15px;
}

.register-link:hover{
    text-decoration:underline;
}

:global(.notification){
    position:fixed;
    top:30px;
    left:50%;
    transform:translateX(-50%) translateY(-20px);
    padding:16px 24px;
    border-radius:10px;
    font-size:16px;
    font-weight:700;
    color:white;
    opacity:0;
    transition:opacity 0.4s ease, transform 0.4s ease;
    z-index:9999;
    max-width:90%;
    text-align:center;
}

:global(.notification.show){
    opacity:1;
    transform:translateX(-50%) translateY(0);
}

:global(.notification.success){
    background:#43a047; /* verde más intenso */
    box-shadow:0 6px 20px rgba(67,160,71,0.4);
}
:global(.notification.error){
    background:#d32f2f; /* rojo más intenso */
    box-shadow:0 6px 20px rgba(211,47,47,0.4);
}
.password-wrapper{
    position:relative;
}

.password-wrapper input{
    width:100%;
    padding:12px;
    border-radius:10px;
    border:1px solid #cfd8dc;
    font-size:14px;
    background:rgba(255,255,255,0.8);
}

.toggle-password{
    position:absolute;
    left:415px;
    top:65%;
    transform:translateY(-50%);
    cursor:pointer;
    font-size:18px;
    color:#1976d2;
    user-select:none;
}
</style>
