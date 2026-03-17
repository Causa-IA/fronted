<script>
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import HamburgerMenu from "$lib/HamburgerMenu.svelte";

  let consulta = null;
  const API_URL = "https://fastapi1-production-5179.up.railway.app";

  onMount(async () => {
    if (!browser) return;

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!id) {
      console.error("No se recibió id en la URL");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/consultas/get_consulta/${id}`);
      const data = await response.json();
      consulta = data.resultado || data;
    } catch (error) {
      console.error("Error cargando consulta:", error);
    }
  });

  function volver() {
    window.location.href = "/consultas_list"; 
  }
</script>

<HamburgerMenu />

<div class="container">
  {#if consulta}
    <h1>Detalle de consulta</h1>

    <div class="card fade-in">
      <h2>Información general</h2>
      <p><b>ID:</b> {consulta.id_consulta}</p>
      <p><b>Motivo:</b> {consulta.motivo_consulta}</p>
      <p><b>Diagnóstico:</b> {consulta.diagnostico}</p>
      <p><b>Observaciones:</b> {consulta.observaciones}</p>
    </div>

    <div class="card fade-in">
      <h2>Signos Vitales</h2>
      <ul>
        <li><b>Presión arterial:</b> {consulta.presion_arterial}</li>
        <li><b>Temperatura:</b> {consulta.temperatura}</li>
        <li><b>Peso:</b> {consulta.peso}</li>
        <li><b>Altura:</b> {consulta.altura}</li>
        <li><b>Saturación:</b> {consulta.saturacion_oxigeno}</li>
        <li><b>Frecuencia cardíaca:</b> {consulta.frecuencia_cardiaca}</li>
        <li><b>Tipo sangre:</b> {consulta.tipo_sangre}</li>
      </ul>
    </div>

    <button on:click={volver}>⬅ Volver</button>
  {:else}
    <p class="loading">Cargando consulta...</p>
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
  max-width: clamp(320px, 90%, 700px);
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

h2{
  margin-bottom:12px;
  color:#1976d2;
  font-size:18px;
}

.card{
  background:white;
  padding:20px;
  border-radius:12px;
  box-shadow:0 6px 20px rgba(0,0,0,0.1);
  margin-bottom:20px;
  transition: transform 0.2s ease;
}

.card:hover{
  transform:scale(1.01);
}

.card p, .card li{
  margin:6px 0;
  font-size:14px;
  color:#333;
}

ul{
  list-style:none;
  padding:0;
}

button {
  display: block;
  margin: 20px auto;
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s ease;
}

button:hover{
  background:#1565c0;
  transform:scale(1.02);
}

button:active{
  transform:scale(0.98);
}

.loading{
  text-align:center;
  font-size:15px;
  color:#1976d2;
}

.fade-in{
  animation: fadeIn 0.6s ease forwards;
}

@keyframes fadeIn{
  from{opacity:0; transform:translateY(10px);}
  to{opacity:1; transform:translateY(0);}
}
</style>
