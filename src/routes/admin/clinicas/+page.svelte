<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '$lib/Tabla.svelte';
  import Modal from '$lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let clinicas = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    nombre: '',
    ubicacion: '',
  });

  onMount(async () => {
    await cargarClinicas();
    loading = false;
  });

  async function cargarClinicas() {
    try {
      const res = await fetch(`${API}/clinicas/get_clinicas/`);
      const data = await res.json();
      clinicas = data.resultado ?? [];
    } catch {
      error = 'Error al cargar clínicas';
    }
  }

  function abrirModal() {
    form = { nombre: '', ubicacion: '' };
    modalAbierto = true;
  }

  async function crearClinica() {
    guardando = true;
    try {
      const res = await fetch(`${API}/clinicas/create_clinica`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        await cargarClinicas();
        modalAbierto = false;
      } else {
        alert('Error al crear la clínica');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  const columnas = [
    { label: 'Nombre',    key: 'nombre' },
    { label: 'Ubicación', key: 'ubicacion' },
  ];
</script>

<div class="page">
  <div class="top">
  <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Clínicas</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar clínica</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={clinicas}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/clinicas/${item.id_clinica}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar clínica"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearClinica}
  {guardando}
>
  <div class="campo">
    <label for="nombre">Nombre</label>
    <input id="nombre" type="text" bind:value={form.nombre} />
  </div>

  <div class="campo">
    <label for="ubicacion">Ubicación</label>
    <input id="ubicacion" type="text" bind:value={form.ubicacion} />
  </div>
</Modal>

<style>
  .page { padding: 2rem; }

  .top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  h2 { font-size: 18px; font-weight: 500; margin: 0; }

  .btn-agregar {
    font-size: 13px;
    padding: 7px 14px;
    border: none;
    border-radius: 8px;
    background: #111827;
    color: white;
    cursor: pointer;
  }

  .btn-agregar:hover { background: #1f2937; }

  .estado { text-align: center; color: #6b7280; padding: 2rem; }
  .estado.error { color: #dc2626; }

  .campo { display: flex; flex-direction: column; gap: 4px; margin-bottom: 1rem; }

  .campo label { font-size: 12px; font-weight: 500; color: #374151; }

  .campo input {
    padding: 7px 10px;
    font-size: 13px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    outline: none;
    background: white;
  }

  .campo input:focus { border-color: #d1d5db; }
</style>