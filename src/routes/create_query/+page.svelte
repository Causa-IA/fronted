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

let id_usuario = "";
let diagnostico = "";
let observaciones = "";
let motivo_consulta = "";
let fecha_entrada = "";
let fecha_salida = "";

let presion_arterial = "";
let temperatura = "";
let peso = "";
let altura = "";
let saturacion_oxigeno = "";
let frecuencia_cardiaca = "";
let tipo_sangre = "";


let menuAbierto = false;
function toggleMenu() {
    menuAbierto = !menuAbierto;
}


const API_URL = "https://fastapi1-3jjn.onrender.com";

onMount(async () => {

    if(browser){

        const params = new URLSearchParams(window.location.search);
        cedula = params.get("cedula");

        if(cedula){
            await cargarEstudiante();
        }

        await cargarUsuarios();

    }

});

async function cargarUsuarios(){
    try{
        const response = await fetch(`${API_URL}/usuarios/get_usuarios/`);
        const data = await response.json();
        usuarios = data.resultado;
    }catch(error){
        console.error("Error cargando usuarios", error);
    }
}

async function cargarEstudiante(){

    try{

        const response = await fetch(`${API_URL}/estudiantes/get_estudiante/${cedula}`);

        if(!response.ok){
            console.error("Estudiante no encontrado");
            return;
        }

        const data = await response.json();

        estudiante = data.resultado || data;

        id_estudiante = estudiante.id_estudiante;
        nombre_estudiante = estudiante.primer_nombre + " " + estudiante.primer_apellido;
        cedula_estudiante = estudiante.numero_identificacion;

    }catch(error){
        console.error("Error cargando estudiante", error);
    }

}

async function guardarConsulta(event){

    event.preventDefault();

    const consultaData = {
        id_estudiante,
        id_usuario,
        diagnostico,
        observaciones,
        motivo_consulta,
        fecha_entrada,
        fecha_salida
    };

    try{

        console.log("Datos enviados:", consultaData);

        const responseConsulta = await fetch(`${API_URL}/consultas/create_consulta`,{
            method:"POST",
            headers:{ "Content-Type":"application/json"},
            body:JSON.stringify(consultaData)
        });

        const dataConsulta = await responseConsulta.json();

        console.log("Respuesta consulta:", dataConsulta);

        if(!responseConsulta.ok){
            showNotification("❌ Error al guardar consulta", "error");
            return;
        }

        const id_consulta = dataConsulta.id_consulta;

        if(!id_consulta){
            showNotification("❌ No se obtuvo ID de consulta", "error");
            return;
        }

        const signosData = {
            id_consulta,
            presion_arterial,
            temperatura: parseFloat(temperatura),
            peso: parseFloat(peso),
            altura: parseFloat(altura),
            saturacion_oxigeno: parseFloat(saturacion_oxigeno),
            frecuencia_cardiaca: parseFloat(frecuencia_cardiaca),
            tipo_sangre
        };

        const responseSignos = await fetch(`${API_URL}/signos_vitales/create_signos`,{
            method:"POST",
            headers:{ "Content-Type":"application/json"},
            body:JSON.stringify(signosData)
        });

        const dataSignos = await responseSignos.json();

        console.log("Respuesta signos:", dataSignos);

        if(responseSignos.ok){
            showNotification("✅ Consulta y signos vitales guardados", "success");
            setTimeout(() => window.location.href = "/search_student", 500);
        }else{
            showNotification("⚠️ Consulta guardada pero signos no", "error");
        }

    }catch(error){
        console.error("Error guardando consulta:", error);
        showNotification("❌ Error del servidor", "error");
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

<h1>Nueva Consulta</h1>

{#if estudiante}

<div class="info">
<p><strong>Estudiante:</strong> {nombre_estudiante}</p>
<p><strong>Cédula:</strong> {cedula_estudiante}</p>
</div>

{/if}

<form on:submit={guardarConsulta}>

<div>
<label>Fecha de entrada
<input type="datetime-local" bind:value={fecha_entrada}>
</label>
</div>

<div>
<label>Enfermera que registra la consulta
<select bind:value={id_usuario} required>
<option value="">Seleccione usuario</option>
{#each usuarios as usuario}
<option value={usuario.id_usuario}>
{usuario.primer_nombre + " " + usuario.primer_apellido}
</option>
{/each}
</select>
</label>
</div>

<div>
  <label>Motivo de consulta
    <textarea bind:value={motivo_consulta} placeholder="Motivo de consulta"></textarea>
  </label>
</div>

<div>
  <label>Diagnóstico
    <textarea bind:value={diagnostico} placeholder="Diagnóstico"></textarea>
  </label>
</div>

<div>
  <label>Observaciones
    <textarea bind:value={observaciones} placeholder="Observaciones"></textarea>
  </label>
</div>

<div class="titulo-seccion">
<h2>Signos Vitales</h2>
</div>

<div>
<label>Presión arterial
<input type="text" bind:value={presion_arterial} placeholder="120/80">
</label>
</div>

<div>
<label>Temperatura (°C)
<input type="number" step="0.1" bind:value={temperatura}>
</label>
</div>

<div>
<label>Peso (kg)
<input type="number" step="0.1" bind:value={peso}>
</label>
</div>

<div>
<label>Altura (m)
<input type="number" step="0.01" bind:value={altura}>
</label>
</div>

<div>
<label>Saturación de oxígeno (%)
<input type="number" step="0.1" bind:value={saturacion_oxigeno}>
</label>
</div>

<div>
<label>Frecuencia cardíaca
<input type="number" bind:value={frecuencia_cardiaca}>
</label>
</div>

<div>
<label>Tipo de sangre
<select bind:value={tipo_sangre}>
<option value="">Seleccione</option>
<option>A+</option>
<option>A-</option>
<option>B+</option>
<option>B-</option>
<option>AB+</option>
<option>AB-</option>
<option>O+</option>
<option>O-</option>
</select>
</label>
</div>

<div>
<label>Fecha de salida
<input type="datetime-local" bind:value={fecha_salida}>
</label>
</div>

<button type="submit">Guardar Consulta</button>

</form>

<button class="rojo">¡¡¡¡EMERGENCIAS!!!!</button>

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


.rojo{
background:red;
margin-top:30px;
}

.rojo:hover{
background:#b71c1c;
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
