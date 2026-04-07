<script>
  let primer_nombre = "";
  let primer_apellido = "";
  let email = "";
  let password = "";
  let showPassword = false; 

  async function register(event) {
    event.preventDefault();

    const usuario = { primer_nombre, primer_apellido, email, password };

    try {
      const response = await fetch("https://fastapi1-3jjn.onrender.com/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(usuario)
      });

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        showNotification("✅ Usuario registrado correctamente", "success");
        setTimeout(() => window.location.href = "/", 1000);
      } else {
        showNotification(data.detail || "❌ Error al registrar usuario", "error");
      }
    } catch (error) {
      console.error(error);
      showNotification("⚠️ Error de conexión", "error");
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

<div id="notification" class="notification"></div>

<div class="container">
  <h1>Registro de usuario</h1>

  <form on:submit={register}>
    <div>
      <label>Nombre
        <input type="text" bind:value={primer_nombre} required>
      </label>
    </div>

    <div>
      <label>Apellido
        <input type="text" bind:value={primer_apellido} required>
      </label>
    </div>

    <div>
      <label>Email
        <input type="email" bind:value={email} required>
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

    <button type="submit">Registrarse</button>
  </form>
  <button class="volver" on:click={() => window.location.href = "/"}>⬅ Volver</button>
</div>

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
  max-width:500px;
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
  background:#43a047;
  box-shadow:0 6px 20px rgba(67,160,71,0.4);
}

:global(.notification.error){
  background:#d32f2f;
  box-shadow:0 6px 20px rgba(211,47,47,0.4);
}

.password-wrapper{
  position:relative;
}

.password-wrapper input{
  width:95%;
  padding:12px;
  border-radius:10px;
  border:1px solid #cfd8dc;
  font-size:14px;
  background:rgba(255,255,255,0.8);
  padding-right:40px; 
}

.toggle-password{
  position:absolute;
  left:490px;
  top:68%;
  transform:translateY(-50%);
  cursor:pointer;
  font-size:18px;
  color:#1976d2;
  user-select:none;
}
.volver {
  margin-top: 10px;
  padding: 12px;
  background: #9e9e9e; 
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s ease;
  width: 100%;
}

.volver:hover {
  background: #757575;
  transform: scale(1.02);
}

.volver:active {
  transform: scale(0.98);
}
</style>
