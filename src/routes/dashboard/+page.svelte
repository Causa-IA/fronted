<script>
  import { onMount } from 'svelte';
  import HamburgerMenu from "$lib/HamburgerMenu.svelte";
  import CerrarSesion from '$lib/CerrarSesion.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let loading = true;
  let error = '';

  let totalConsultas = 0;
  let totalEstudiantes = 0;
  let totalEmergencias = 0;

  let nombreUsuario = 'Administrador';

  onMount(async () => {
    const stored = localStorage.getItem('session');
    if (stored) {
      const s = JSON.parse(stored);
      nombreUsuario = s.nombre || 'Administrador';
    }

    try {
      const [resConsultas, resEstudiantes, resEmergencias] = await Promise.all([
        fetch(`${API}/consultas/get_consultas/`),
        fetch(`${API}/estudiantes/get_estudiantes/`),
        fetch(`${API}/emergencias/get_emergencias/`)
      ]);

      if (!resConsultas.ok || !resEstudiantes.ok || !resEmergencias.ok) {
        throw new Error('Error al cargar datos del servidor');
      }

      const consultas   = (await resConsultas.json()).resultado;
      const estudiantes = (await resEstudiantes.json()).resultado;
      const emergencias = (await resEmergencias.json()).resultado;

      totalConsultas   = consultas.length;
      totalEstudiantes = estudiantes.length;
      totalEmergencias = emergencias.length;

      loading = false;

    } catch (e) {
      error = e.message;
      loading = false;
    }
  });
</script>


  <HamburgerMenu />
  <CerrarSesion />

  {#if loading}
    <div class="center-msg">
      <div class="spinner"></div>
      <p>Cargando estadísticas...</p>
    </div>

  {:else if error}
    <div class="center-msg error-msg">
      <p>⚠️ {error}</p>
      <button on:click={() => location.reload()}>Reintentar</button>
    </div>

  {:else}
    <section class="cards">
      <div class="card">
        <span class="card-icon">🩺</span>
        <div>
          <p class="card-label">Total Consultas</p>
          <p class="card-value">{totalConsultas}</p>
        </div>
      </div>
      <div class="card">
        <span class="card-icon">🎓</span>
        <div>
          <p class="card-label">Total Estudiantes</p>
          <p class="card-value">{totalEstudiantes}</p>
        </div>
      </div>
      <div class="card">
        <span class="card-icon">🚨</span>
        <div>
          <p class="card-label">Total Emergencias</p>
          <p class="card-value">{totalEmergencias}</p>
        </div>
      </div>
    </section>

    <!-- ✅ iframe de Power BI -->
    <section class="powerbi-section">
      <div class="chart-box">
        <h2>📊 Reporte Power BI</h2>
        <div class="powerbi-wrapper">
          <iframe
            title="enfermeras"
            src="https://app.powerbi.com/reportEmbed?reportId=42bd2357-3477-44af-b14e-acd1a93cd941&autoAuth=true&ctid=740be6bd-fd36-470e-94d9-0f0c777fadb9"
            frameborder="0"
            allowfullscreen="true"
          ></iframe>
        </div>
      </div>
    </section>
  {/if}


<style>
  :global(body) {
    margin: 0;
    background: #0f172a;
    font-family: 'Segoe UI', sans-serif;
    color: #e2e8f0;
  }


  /* Cards */
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.2rem;
    margin-bottom: 2rem;
  }
  .card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99,179,237,0.15);
  }
  .card-icon { font-size: 2rem; }
  .card-label {
    margin: 0;
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .card-value {
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f0;
  }

  /* Power BI */
  .powerbi-section {
    margin-top: 1.5rem;
  }
  .chart-box {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
  }
  .chart-box h2 {
    margin: 0 0 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #cbd5e1;
  }
  .powerbi-wrapper {
    position: relative;
    width: 100%;
    /* Mantiene proporción 1140x541 de Power BI */
    padding-top: 47.5%;
  }
  .powerbi-wrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
    border-radius: 10px;
  }

  /* Mensajes */
  .center-msg {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 50vh;
    gap: 1rem;
    color: #94a3b8;
  }
  .error-msg { color: #f87171; }
  .error-msg button {
    background: rgba(248,113,113,0.15);
    border: 1px solid #f87171;
    color: #f87171;
    padding: 0.5rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
  }
  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(99,179,237,0.2);
    border-top-color: #63b3ed;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>