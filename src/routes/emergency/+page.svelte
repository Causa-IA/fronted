<script>
import { onMount } from "svelte";
import { browser } from "$app/environment";
import HamburgerMenu from "$lib/HamburgerMenu.svelte";

let estudiante = null;
let nombre_estudiante = "";
let cedula_estudiante = "";
let id_estudiante = null;
let cedula = null;

let usuarios = [];
let clinicas = [];

let id_usuario = "";
let fecha = "";
let descripcion = "";
let atencion_prestada = "";

// Derivaciones
let id_clinica = "";
let razon = "";
let fecha_derivacion = "";

const API_URL = "https://fastapi1-production-5179.up.railway.app";

onMount(async () => {
    if(browser){
        const params = new URLSearchParams(window.location.search);
        cedula = params.get("cedula");
        if(cedula) await cargarEstudiante();
        await cargarUsuarios();
        await cargarClinicas();
    }
});

async function cargarUsuarios(){
    const res = await fetch(`${API_URL}/usuarios/get_usuarios/`);
    const data = await res.json();
    usuarios = data.resultado;
}

async function cargarClinicas(){
    const res = await fetch(`${API_URL}/clinicas/get_clinicas/`);
    const data = await res.json();
    clinicas = data.resultado;
}

async function cargarEstudiante(){
    const res = await fetch(`${API_URL}/estudiantes/get_estudiante/${cedula}`);
    const data = await res.json();
    estudiante = data.resultado || data;
    id_estudiante = estudiante.id_estudiante;
    nombre_estudiante = estudiante.primer_nombre + " " + estudiante.primer_apellido;
    cedula_estudiante = estudiante.numero_identificacion;
}

async function guardarEmergencia(event){
    event.preventDefault();

    const emergenciaData = {
        id_estudiante,
        id_usuario,
        fecha,
        descripcion,
        atencion_prestada
    };

    const resEmergencia = await fetch(`${API_URL}/emergencias/create_emergencia`, {
        method:"POST",
        headers:{ "Content-Type":"application/json"},
        body:JSON.stringify(emergenciaData)
    });

    const dataEmergencia = await resEmergencia.json();
    const id_emergencia = dataEmergencia.id_emergencia;

    if(!id_emergencia){
        showNotification("❌ Error al guardar emergencia", "error");
        return;
    }

    // Guardar derivación
    const derivacionData = {
        id_emergencia,
        id_clinica,
        razon,
        fecha: fecha_derivacion
    };

    const resDerivacion = await fetch(`${API_URL}/derivaciones/create_derivacion`, {
        method:"POST",
        headers:{ "Content-Type":"application/json"},
        body:JSON.stringify(derivacionData)
    });

    if(resDerivacion.ok){
        showNotification("✅ Emergencia y derivación guardadas", "success");
        setTimeout(() => window.location.href = "/search_student", 500);
    }else{
        showNotification("⚠️ Emergencia guardada pero derivación no", "error");
    }
}

function showNotification(message, type){
    const notif = document.getElementById("notification");
    notif.textContent = message;
    notif.className = "notification show " + type;
    setTimeout(()=> notif.classList.remove("show"), 500);
}
</script>

<div id="notification" class="notification"></div>
<HamburgerMenu />

<div class="container">
<h1>Nueva Emergencia</h1>

{#if estudiante}
<div class="info">
<p><strong>Estudiante:</strong> {nombre_estudiante}</p>
<p><strong>Cédula:</strong> {cedula_estudiante}</p>
</div>
{/if}

<form on:submit={guardarEmergencia}>
  <div>
    <label>Fecha
      <input type="datetime-local" bind:value={fecha}>
    </label>
  </div>

  <div>
    <label>Enfermera
      <select bind:value={id_usuario} required>
        <option value="">Seleccione enfermera</option>
        {#each usuarios as usuario}
          <option value={usuario.id_usuario}>
            {usuario.primer_nombre} {usuario.primer_apellido}
          </option>
        {/each}
      </select>
    </label>
  </div>

  <div>
    <label>Descripción
      <textarea bind:value={descripcion}></textarea>
    </label>
  </div>

  <div>
    <label>Atención prestada
      <textarea bind:value={atencion_prestada}></textarea>
    </label>
  </div>

  <div class="titulo-seccion">
    <h2>Derivaciones</h2>
  </div>

  <div>
    <label>Clínica
      <select bind:value={id_clinica}>
        <option value="">Seleccione clínica</option>
        {#each clinicas as clinica}
          <option value={clinica.id_clinica}>{clinica.nombre}</option>
        {/each}
      </select>
    </label>
  </div>

  <div>
    <label>Razón
      <textarea bind:value={razon}></textarea>
    </label>
  </div>

  <div>
    <label>Fecha derivación
      <input type="datetime-local" bind:value={fecha_derivacion}>
    </label>
  </div>

  <button type="submit">Guardar Emergencia</button>
</form>
</div>
<style>
*{
  box-sizing:border-box;
}

:global(body){
  background: linear-gradient(135deg,#eff2f5,rgb(222,227,240));
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;
}

.container{
  max-width: clamp(320px,90%,750px);
  width:100%;
  padding:25px;
  border-radius:20px;
  background:rgba(255,255,255,0.25);
  box-shadow:0 8px 32px rgba(0,0,0,0.15);
  backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.18);
}

h1{
  text-align:center;
  margin:0;
  color:#1a237e;
  font-weight:700;
}

.info{
  background:white;
  padding:15px;
  margin-top:20px;
  border-radius:10px;
  box-shadow:0 5px 15px rgba(0,0,0,0.08);
}

form{
  background:white;
  padding:30px;
  border-radius:12px;
  width:100%;
  margin-top:20px;
}

form div{
  margin-bottom:18px;
}

label{
  display:block;
  font-size:14px;
  font-weight:600;
  color:#34495e;
  margin-bottom:6px;
}

input, select{
  width:100%;
  padding:15px 12px;
  border-radius:8px;
  border:1px solid #dcdfe6;
  font-size:14px;
  transition:all 0.2s ease;
}

input:focus, select:focus{
  outline:none;
  border-color:#2f80ed;
  box-shadow:0 0 0 2px rgba(47,128,237,0.15);
}

button{
  display:block;
  margin:15px auto;
  padding:12px 24px;
  background:#1976d2;
  color:white;
  border:none;
  border-radius:10px;
  font-size:15px;
  font-weight:600;
  cursor:pointer;
  transition:transform 0.2s ease,background 0.3s ease;
}

button:hover{
  background:#1565c0;
  transform:scale(1.02);
}

@media (min-width:600px){
  form{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
  }
  form div{
    margin-bottom:0;
  }
  button{
    grid-column:span 2;
    width:100%;
  }
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

.titulo-seccion{
  grid-column: span 2;
  margin-top:10px;
}

.titulo-seccion h2{
  margin:0;
  color:#1a237e;
  font-size:18px;
}

textarea {
  width: 100%;
  min-height: 80px;   
  padding: 15px 12px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 14px;
  resize: vertical;   
  transition: all 0.2s ease;
}

textarea:focus {
  outline: none;
  border-color: #2f80ed;
  box-shadow: 0 0 0 2px rgba(47,128,237,0.15);
}
</style>