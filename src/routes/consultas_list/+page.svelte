<script>
  import { onMount } from "svelte";
  import HamburgerMenu from "$lib/HamburgerMenu.svelte";

  let cedula = "";
  let consultas = [];
  const API_URL = "https://fastapi1-3jjn.onrender.com";

  async function obtenerNombreEstudiante(id_estudiante) {
  try {
    const response = await fetch(`${API_URL}/estudiantes/${id_estudiante}`);
    const data = await response.json();
    return `${data.primer_nombre} ${data.primer_apellido}`;
  } catch (error) {
    console.error("Error obteniendo estudiante:", error);
    return "Estudiante desconocido";
  }
  }

  async function buscarConsultas() {
  if (!cedula) {
    consultas = [];
    return;
  }
  try {
    const response = await fetch(`${API_URL}/consultas/get_consultas/${cedula}`);
    const data = await response.json();
    consultas = (data.resultado || []).sort((a, b) =>
      new Date(b.fecha_entrada) - new Date(a.fecha_entrada)
    );
  } catch (error) {
    console.error("Error consultando API:", error);
  }
}


  async function cargarConsultasIniciales() {
  try {
    const response = await fetch(`${API_URL}/consultas/get_consultas/`);
    const data = await response.json();
    console.log("Respuesta inicial:", data);

    if (Array.isArray(data.resultado)) {
      consultas = data.resultado.sort((a, b) =>
        new Date(b.fecha_entrada) - new Date(a.fecha_entrada)
      );
    } else if (data.resultado) {
      consultas = [data.resultado];
    } else {
      consultas = [];
    }
  } catch (error) {
    console.error("Error cargando consultas iniciales:", error);
  }
}



  function verConsulta(id) {
    window.location.href = `/consulta_detail?id=${id}`;
  }

  function formatDate(fecha) {
    if (!fecha) return "";
    const d = new Date(fecha);
    return d.toLocaleDateString("es-CO", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  onMount(() => {
    cargarConsultasIniciales();
  });

  
</script>

<HamburgerMenu />
<div class="container fade-in">
  <h1>Lista de Consultas</h1>

  <div class="search-box">
    <input
      type="text"
      placeholder="Buscar por cédula"
      bind:value={cedula}
      on:keydown={(e) => {
        if (e.key === "Enter") {
          buscarConsultas();
        }
      }}
    />
    <button on:click={buscarConsultas}>Buscar</button>
  </div>

  {#if consultas.length > 0}
    <table>
      <thead>
        <tr>
          <th>Estudiante</th>
          <th>Fecha entrada</th>
          <th>Fecha salida</th>
          <th>Motivo</th>
          <th>Diagnóstico</th>
        </tr>
      </thead>
      <tbody>
        {#each consultas as consulta}
          <tr on:click={() => verConsulta(consulta.id_consulta)}>
            <td>{consulta.primer_nombre} {consulta.primer_apellido}</td>
            <td><span class="fecha">{formatDate(consulta.fecha_entrada)}</span></td>
            <td><span class="fecha">{formatDate(consulta.fecha_salida)}</span></td>
            <td>{consulta.motivo_consulta}</td>
            <td>{consulta.diagnostico}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <p class="no-results">❌ No hay consultas registradas</p>
  {/if}
</div>

<style>
:global(body){
  margin:0;
  font-family:"Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background:linear-gradient(135deg, #eff2f5, rgb(222,227,240));
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:flex-start;
}

.container{
  margin-top:60px;
  width:90%;
  max-width:900px;
  padding:30px;
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

.search-box{
  display:flex;
  justify-content:center;
  gap:10px;
  margin-bottom:25px;
}

.search-box input{
  width:260px;
  padding:12px;
  border-radius:10px;
  border:1px solid #cfd8dc;
  background:rgba(255,255,255,0.8);
  font-size:14px;
  transition:all 0.3s ease;
}

.search-box input:focus{
  outline:none;
  border-color:#1976d2;
  box-shadow:0 0 0 3px rgba(25,118,210,0.2);
}

.search-box button{
  padding:12px 24px;
  border:none;
  border-radius:10px;
  background:#1976d2;
  color:white;
  font-weight:600;
  cursor:pointer;
  transition:transform 0.2s ease, background 0.3s ease;
}

.search-box button:hover{
  background:#1565c0;
  transform:scale(1.02);
}

table{
  width:100%;
  border-collapse:collapse;
  background:white;
  border-radius:12px;
  overflow:hidden;
  box-shadow:0 6px 20px rgba(0,0,0,0.1);
}

thead{
  background:#0f172a;
  color:white;
}

th, td{
  padding:12px;
  text-align:left;
  font-size:14px;
}

tbody tr{
  transition:background 0.2s ease;
  cursor:pointer;
}

tbody tr:hover{
  background:#f1f5f9;
}

.no-results{
  text-align:center;
  margin-top:20px;
  font-size:15px;
  color:#d32f2f;
  font-weight:600;
}

.fade-in{
  animation:fadeIn 0.6s ease forwards;
}

@keyframes fadeIn{
  from{opacity:0; transform:translateY(10px);}
  to{opacity:1; transform:translateY(0);}
}

.fecha {
  display:inline-block;
  padding:4px 8px;
  background:#e3f2fd;
  color:#0d47a1;
  border-radius:6px;
  font-size:13px;
  font-weight:600;
}
</style>
