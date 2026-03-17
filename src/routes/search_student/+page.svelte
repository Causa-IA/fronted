<script>
  import HamburgerMenu from "$lib/HamburgerMenu.svelte";
  let tipo_identificacion;
  let numero_identificacion;
  let estudiante = null;
  let encontrado = null;

  async function search_student(event) {
    event.preventDefault();

    try {
      const response = await fetch(`https://fastapi1-production-5179.up.railway.app/estudiantes/get_estudiante/${numero_identificacion}`);

      if (response.ok) {
        const data = await response.json();
        estudiante = data.resultado ? data.resultado : data;
        encontrado = true;
        showNotification("✅ Estudiante encontrado", "success");
      } else if (response.status === 404) {
        estudiante = null;
        encontrado = false;
        showNotification("❌ Estudiante no encontrado", "error");
      } else {
        showNotification("⚠️ Error del servidor", "error");
      }
    } catch (error) {
      console.error("Error en fetch:", error);
      showNotification("⚠️ Error de conexión", "error");
    }
  }

  function nuevaConsulta() {
  if (estudiante) {
    window.location.href = `/create_query?cedula=${estudiante.numero_identificacion}`;
  }
}

  function registrarEstudiante() {
    window.location.href = "/create_students";
  }

  function showNotification(message, type) {
    const notif = document.getElementById("notification");
    notif.textContent = message;
    notif.className = "notification show " + type;
    setTimeout(() => notif.classList.remove("show"), 1000);
  }
</script>

<HamburgerMenu />
<div id="notification" class="notification"></div>

<div class="container">
  <h1>Buscar estudiante</h1>

  <form on:submit={search_student}>
    <div>
      <label>Tipo de documento
        <select bind:value={tipo_identificacion}>
          <option value="CC">Cédula de Ciudadanía</option>
          <option value="TI">Tarjeta de Identidad</option>
          <option value="CE">Cédula de Extranjería</option>
        </select>
      </label>
    </div>
    
    <div>
      <label>Documento de identidad
        <input type="text" placeholder="Ingrese el número de documento" bind:value={numero_identificacion}>
      </label>
    </div>
    
    <button type="submit">Buscar estudiante</button>
  </form>

  {#if encontrado === true && estudiante}
  <div class="card">
    <h2>{estudiante.primer_nombre} {estudiante.primer_apellido}</h2>
    <p><strong>Tipo de Identificación:</strong> {estudiante.tipo_identificacion}</p>
    <p><strong>Número:</strong> {estudiante.numero_identificacion}</p>
    <p><strong>Género:</strong> {estudiante.genero}</p>
    <p><strong>Teléfono:</strong> {estudiante.telefono}</p>
    <p><strong>Dirección:</strong> {estudiante.direccion}</p>
    <p><strong>Fecha de Registro:</strong> {estudiante.fecha_registro}</p>
    
    <div class="acciones">
      <button on:click={nuevaConsulta}>Crear nueva consulta</button>
      <button class="rojo" on:click={() => window.location.href=`/emergency?cedula=${estudiante.numero_identificacion}`}>
        ¡¡EMERGENCIA!!
      </button>
    </div>
  </div>
  {:else if encontrado === false}
    <p class="not-found">Estudiante no encontrado</p>
    <button on:click={registrarEstudiante}>Registrar estudiante</button>
  {/if}
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
  max-width: clamp(320px, 90%, 600px);
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
  margin-bottom:20px;
}

form div{
  margin-bottom:18px;
}

label{
  font-size:14px;
  font-weight:600;
  color:#1a237e;
  margin-bottom:6px;
  display:block;
}

input, select{
  width:100%;
  padding:12px;
  border-radius:10px;
  border:1px solid #cfd8dc;
  font-size:14px;
  background:rgba(255,255,255,0.8);
  transition:all 0.3s ease;
}

input:focus, select:focus{
  outline:none;
  border-color:#1976d2;
  box-shadow:0 0 0 3px rgba(25,118,210,0.2);
}

button {
  display: block;
  margin: 15px auto;   
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s ease;
  width: auto;         
}

button:hover{
  background:#1565c0;
  transform:scale(1.02);
}

button:active{
  transform:scale(0.98);
}

.card{
  background:white;
  padding:20px;
  border-radius:12px;
  box-shadow:0 6px 20px rgba(0,0,0,0.1);
  margin-top:20px;
}

.card h2{
  margin-bottom:12px;
  color:#1976d2;
}

.card p{
  margin:6px 0;
  font-size:14px;
  color:#333;
}

.not-found{
  text-align:center;
  font-size:15px;
  color:#d32f2f;
  margin-bottom:10px;
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
.acciones {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 15px;
}

.rojo {
  background: red;
  color: white;
  font-weight: 700;
}

.rojo:hover {
  background: #b71c1c;
}
</style>
