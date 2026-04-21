<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '$lib/Tabla.svelte';
  import Modal from '$lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let roles = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    nombre: '',
    descripcion: '',
    acceso_privilegiado: false,
  });

  onMount(async () => {
    await cargarRoles();
    loading = false;
  });

  async function cargarRoles() {
    try {
      const res = await fetch(`${API}/roles/get_roles/`);
      const data = await res.json();
      roles = data.resultado ?? [];
    } catch {
      error = 'Error al cargar roles';
    }
  }

  function abrirModal() {
    form = { nombre: '', descripcion: '', acceso_privilegiado: false };
    modalAbierto = true;
  }

  async function crearRol() {
    guardando = true;
    try {
      const res = await fetch(`${API}/roles/create_rol`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        await cargarRoles();
        modalAbierto = false;
      } else {
        alert('Error al crear el rol');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  const columnas = [
    { label: 'Nombre',               key: 'nombre' },
    { label: 'Descripción',          key: 'descripcion' },
    { label: 'Acceso privilegiado',  key: 'acceso_privilegiado' },
  ];
</script>

<div class="page">
  <div class="top">
  <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Roles</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar rol</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={roles}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/roles/${item.id_rol}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar rol"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearRol}
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

  <div class="campo-toggle">
    <span class="toggle-label">Acceso privilegiado</span>
    <button
      class="toggle {form.acceso_privilegiado ? 'activo' : 'inactivo'}"
      onclick={() => form.acceso_privilegiado = !form.acceso_privilegiado}
      type="button"
    >
      <span class="toggle-thumb"></span>
      <span class="toggle-text">{form.acceso_privilegiado ? 'Sí' : 'No'}</span>
    </button>
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

  .campo-toggle { display: flex; flex-direction: column; gap: 4px; }

  .toggle-label { font-size: 12px; font-weight: 500; color: #374151; }

  .toggle {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    background: white;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    width: fit-content;
    transition: all 0.2s;
  }

  .toggle-thumb {
    width: 36px;
    height: 20px;
    border-radius: 20px;
    position: relative;
    transition: background 0.2s;
  }

  .toggle-thumb::after {
    content: '';
    position: absolute;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: white;
    top: 3px;
    transition: left 0.2s;
  }

  .toggle.activo .toggle-thumb { background: #16a34a; }
  .toggle.activo .toggle-thumb::after { left: 19px; }
  .toggle.inactivo .toggle-thumb { background: #d1d5db; }
  .toggle.inactivo .toggle-thumb::after { left: 3px; }
  .toggle.activo { color: #16a34a; border-color: #bbf7d0; }
  .toggle.inactivo { color: #6b7280; border-color: #e5e7eb; }
</style>