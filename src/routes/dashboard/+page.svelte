<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { Chart, registerables } from 'chart.js';
  import HamburgerMenu from "$lib/HamburgerMenu.svelte";

  Chart.register(...registerables);

  const API = 'https://fastapi1-production-5179.up.railway.app';

  let loading = true;
  let error = '';

  let totalConsultas = 0;
  let totalEstudiantes = 0;
  let totalEmergencias = 0;

  let nombreUsuario = 'Administrador';

  let canvasPorEnfermera;
  let canvasPorFecha;
  let chartEnfermera = null;
  let chartFecha = null;

  function agruparPorCampo(lista, campo) {
    return lista.reduce((acc, item) => {
      const key = item[campo] || 'Sin datos';
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
  }

  function agruparPorFecha(consultas) {
    return consultas.reduce((acc, item) => {
      const fecha = item.fecha_entrada
        ? item.fecha_entrada.substring(0, 10)
        : 'Sin fecha';
      acc[fecha] = (acc[fecha] || 0) + 1;
      return acc;
    }, {});
  }

  function crearGraficaBarras(canvas, labels, data, label, color) {
    return new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label,
          data,
          backgroundColor: color,
          borderRadius: 6,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.parsed.y} consultas`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: '#cbd5e1' },
            grid: { color: 'rgba(255,255,255,0.05)' }
          },
          x: {
            ticks: { color: '#cbd5e1', maxRotation: 45 },
            grid: { display: false }
          }
        }
      }
    });
  }

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

      // ← LOGS AQUÍ
      console.log('CONSULTAS:', consultas);
      console.log('ESTUDIANTES:', estudiantes);
      console.log('EMERGENCIAS:', emergencias);

      totalConsultas   = consultas.length;
      totalEstudiantes = estudiantes.length;
      totalEmergencias = emergencias.length;

      const porEnfermera = agruparPorCampo(consultas, 'nombre_enfermera');
      const labelsEnfermera = Object.keys(porEnfermera);
      const dataEnfermera   = Object.values(porEnfermera);

      const porFechaRaw = agruparPorFecha(consultas);
      const fechasOrdenadas = Object.keys(porFechaRaw).sort().slice(-10);
      const dataFecha = fechasOrdenadas.map(f => porFechaRaw[f]);

      loading = false;

      await new Promise(r => setTimeout(r, 0));

      if (chartEnfermera) chartEnfermera.destroy();
      if (chartFecha) chartFecha.destroy();

      chartEnfermera = crearGraficaBarras(
        canvasPorEnfermera, labelsEnfermera, dataEnfermera,
        'Consultas por enfermera', 'rgba(99, 179, 237, 0.8)'
      );

      chartFecha = crearGraficaBarras(
        canvasPorFecha, fechasOrdenadas, dataFecha,
        'Consultas por fecha', 'rgba(154, 117, 234, 0.8)'
      );

    } catch (e) {
      error = e.message;
      loading = false;
    }
  });
</script>


<div class="dashboard">

  <header class="dash-header">
    <h1>Dashboard</h1>
    <span class="usuario-info">👤 {nombreUsuario}</span>
  </header>

  <HamburgerMenu />
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

    <section class="charts">
      <div class="chart-box">
        <h2>Consultas por Enfermera</h2>
        <div class="chart-wrapper">
          <canvas bind:this={canvasPorEnfermera}></canvas>
        </div>
      </div>

      <div class="chart-box">
        <h2>Consultas por Fecha <span class="sub">(últimos 10 días)</span></h2>
        <div class="chart-wrapper">
          <canvas bind:this={canvasPorFecha}></canvas>
        </div>
      </div>
    </section>
  {/if}

</div>

<style>
  :global(body) {
    margin: 0;
    background: #0f172a;
    font-family: 'Segoe UI', sans-serif;
    color: #e2e8f0;
  }

  .dashboard {
    min-height: 100vh;
    padding: 2rem;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  }

  .dash-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  .dash-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #63b3ed, #9a75ea);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .usuario-info {
    font-size: 0.9rem;
    color: #94a3b8;
    background: rgba(255,255,255,0.05);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
  }

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

  .charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 1.5rem;
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
  .sub {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 400;
  }
  .chart-wrapper {
    position: relative;
    height: 260px;
  }

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