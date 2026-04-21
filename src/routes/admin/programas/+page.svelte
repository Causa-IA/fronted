<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '$lib/Tabla.svelte';
  import Modal from '$lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let programas = $state([]);
  let facultades = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    nombre: '',
    descripcion: '',
    id_facultad: '',
  });

  onMount(async () => {
    await Promise.all([cargarProgramas(), cargarFacultades()]);
    loading = false;
  });

  async function cargarProgramas() {
    try {
      const res = await fetch(`${API}/programas/get_programas/`);
      const data = await res.json();
      programas = data.resultado ?? [];
    } catch {
      error = 'Error al cargar programas';
    }
  }

  async function cargarFacultades() {
    const res = await fetch(`${API}/facultades/get_facultades/`);
    const data = await res.json();
    facultades = data.resultado ?? [];
  }

  function abrirModal() {
    form = { nombre: '', descripcion: '', id_facultad: '' };
    modalAbierto = true;
  }

  async function crearPrograma() {
    guardando = true;
    try {
      const res = await fetch(`${API}/programas/create_programa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          id_facultad: Number(form.id_facultad),
        }),
      });

      if (res.ok) {
        await cargarProgramas();
        modalAbierto = false;
      } else {
        alert('Error al crear el programa');
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
    { label: 'Facultad',    key: 'id_facultad' },
  ];
</script>

<div class="page">
  <div class="top">
  <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Programas</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar programa</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={programas}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/programas/${item.id_programa}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar programa"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearPrograma}
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

  <div class="campo">
    <label for="facultad">Facultad</label>
    <select id="facultad" bind:value={form.id_facultad}>
      <option value="">Seleccionar...</option>
      {#each facultades as f}
        <option value={f.id_facultad}>{f.nombre}</option>
      {/each}
    </select>
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

  .campo input,
  .campo select {
    padding: 7px 10px;
    font-size: 13px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    outline: none;
    background: white;
  }

  .campo input:focus,
  .campo select:focus { border-color: #d1d5db; }
</style>