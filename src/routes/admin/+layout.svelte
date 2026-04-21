<script>
  import CerrarSesion from '$lib/CerrarSesion.svelte';
  let { children } = $props();
</script>

<div class="layout">
  <CerrarSesion />
  <div class="container fade-in">
    {@render children()}
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
    min-height: 100vh;
  }

  :global(h1, h2) {
    color: #1a237e;
    font-weight: 700;
  }

  :global(input), :global(select), :global(textarea) {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #cfd8dc;
    background: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease;
    box-sizing: border-box;
  }

  :global(input:focus), :global(select:focus), :global(textarea:focus) {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
  }

  :global(label) {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 5px;
  }

  :global(.campo) {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 1rem;
  }

  :global(.fila) {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  :global(.btn-primario) {
    padding: 12px 24px;
    border: none;
    border-radius: 10px;
    background: #1976d2;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    transition: transform 0.2s ease, background 0.3s ease;
  }

  :global(.btn-primario:hover) {
    background: #1565c0;
    transform: scale(1.02);
  }

  :global(.btn-primario:disabled) {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  :global(.btn-peligro) {
    padding: 12px 24px;
    border: 1px solid rgba(220, 38, 38, 0.4);
    border-radius: 10px;
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    transition: transform 0.2s ease, background 0.3s ease;
  }

  :global(.btn-peligro:hover) {
    background: rgba(220, 38, 38, 0.2);
    transform: scale(1.02);
  }

  :global(.btn-peligro:disabled) {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  :global(.btn-volver) {
    background: none;
    border: none;
    font-size: 13px;
    color: #546e7a;
    cursor: pointer;
    padding: 0;
    margin-bottom: 6px;
    font-weight: 600;
    display: block;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  :global(.btn-volver:hover) { color: #1a237e; }

  :global(.card-detalle) {
    background: white;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  }

  :global(.seccion-titulo) {
    font-size: 12px;
    font-weight: 700;
    color: #90a4ae;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 1rem;
  }

  :global(.estado-carga) {
    text-align: center;
    padding: 2rem;
    font-size: 15px;
    color: #546e7a;
    font-weight: 600;
  }

  :global(.estado-error) {
    text-align: center;
    padding: 2rem;
    font-size: 15px;
    color: #d32f2f;
    font-weight: 600;
  }

  :global(.top-pagina) {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 12px;
  }

  :global(.acciones) {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }

  .layout {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 60px 20px 40px;
  }

  .container {
    width: 90%;
    max-width: 960px;
    padding: 32px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.18);
  }

  .fade-in {
    animation: fadeIn 0.6s ease forwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @media (max-width: 600px) {
    .layout { padding: 50px 12px 30px; }

    .container { padding: 20px 16px; width: 100%; }

    :global(.fila) { grid-template-columns: 1fr; }

    :global(.top-pagina) { flex-direction: column; }

    :global(.acciones) { width: 100%; justify-content: flex-end; }
  }
</style>