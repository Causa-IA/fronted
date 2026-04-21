<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '$lib/Tabla.svelte';
  import Modal from '$lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let facultades = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    nombre: '',
    descripcion: '',
  });

  onMount(async () => {
    await cargarFacultades();
    loading = false;
  });

  async function cargarFacultades() {
    try {
      const res = await fetch(`${API}/facultades/get_facultades/`);
      const data = await res.json();
      facultades = data.resultado ?? [];
    } catch {
      error = 'Error al cargar facultades';
    }
  }

  function abrirModal() {
    form = { nombre: '', descripcion: '' };
    modalAbierto = true;
  }

  async function crearFacultad() {
    guardando = true;
    try {
      const res = await fetch(`${API}/facultades/create_facultad`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        await cargarFacultades();
        modalAbierto = false;
      } else {
        alert('Error al crear la facultad');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  const columnas = [
    { label: 'Nombre',      key: 'nombre' },
    { label: 'Descripción', key: 'descripcion' },
  ];
</script>

<div class="page">
  <div class="top">
  <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Facultades</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar facultad</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={facultades}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/facultad/${item.id_facultad}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar facultad"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearFacultad}
  {guardando}
>
  <div class="campo">
    <label for="nombre">Nombre</label>
    <input id="nombre" type="text" bind:value={form.nombre} />
  </div>

  <div class="campo">
    <label for="descripcion">Descripción</label>
    <input id="descripcion" type="text" bind:value={form.descripcion} />
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