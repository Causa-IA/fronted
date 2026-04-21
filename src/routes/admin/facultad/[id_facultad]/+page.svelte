<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  const API = 'https://fastapi1-3jjn.onrender.com';
  const id_facultad = $page.params.id_facultad;

  let loading = $state(true);
  let guardando = $state(false);
  let eliminando = $state(false);
  let error = $state(null);

  let form = $state({
    id_facultad: '',
    nombre: '',
    descripcion: '',
  });

  onMount(async () => {
    await cargarFacultad();
    loading = false;
  });

  async function cargarFacultad() {
    try {
      const res = await fetch(`${API}/facultades/get_facultad/${id_facultad}`);
      const data = await res.json();
      form = {
        id_facultad: data.id_facultad,
        nombre: data.nombre,
        descripcion: data.descripcion,
      };
    } catch {
      error = 'Error al cargar la facultad';
    }
  }

  async function guardar() {
    guardando = true;
    try {
      const res = await fetch(`${API}/facultades/${form.id_facultad}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        alert('Facultad actualizada correctamente');
      } else {
        alert('Error al actualizar la facultad');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  async function eliminar() {
    const confirmar = confirm('¿Estás seguro de que deseas eliminar esta facultad?');
    if (!confirmar) return;

    eliminando = true;
    try {
      const res = await fetch(`${API}/facultades/${form.id_facultad}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        goto('/admin/facultad');
      } else {
        alert('Error al eliminar la facultad');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      eliminando = false;
    }
  }
</script>

<div class="page">
  {#if loading}
    <p class="estado">Cargando...</p>

  {:else if error}
    <p class="estado error">{error}</p>

  {:else}
    <div class="top">
      <div>
        <button class="btn-volver" onclick={() => goto('/admin/facultad')}>← Volver</button>
        <h2>{form.nombre}</h2>
        <p class="sub">{form.descripcion}</p>
      </div>
      <div class="acciones">
        <button class="btn-eliminar" onclick={eliminar} disabled={eliminando}>
          {eliminando ? 'Eliminando...' : 'Eliminar'}
        </button>
        <button class="btn-guardar" onclick={guardar} disabled={guardando}>
          {guardando ? 'Guardando...' : 'Guardar cambios'}
        </button>
      </div>
    </div>

    <div class="card">
      <p class="seccion-titulo">Información de la facultad</p>

      <div class="campo">
        <label for="nombre">Nombre</label>
        <input id="nombre" type="text" bind:value={form.nombre} />
      </div>

      <div class="campo">
        <label for="descripcion">Descripción</label>
        <input id="descripcion" type="text" bind:value={form.descripcion} />
      </div>
    </div>
  {/if}
</div>

<style>
  .page { padding: 2rem; max-width: 720px; }

  .top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }

  .btn-volver {
    font-size: 12px;
    color: #6b7280;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-bottom: 6px;
    display: block;
  }

  .btn-volver:hover { color: #111827; }

  h2 { font-size: 20px; font-weight: 500; margin: 0; }
  .sub { font-size: 13px; color: #6b7280; margin: 2px 0 0; }

  .acciones { display: flex; gap: 8px; align-items: center; }

  .btn-eliminar {
    font-size: 13px;
    padding: 7px 14px;
    border: 1px solid #fee2e2;
    border-radius: 8px;
    background: white;
    color: #dc2626;
    cursor: pointer;
  }

  .btn-eliminar:hover { background: #fee2e2; }
  .btn-eliminar:disabled { opacity: 0.5; cursor: not-allowed; }

  .btn-guardar {
    font-size: 13px;
    padding: 7px 14px;
    border: none;
    border-radius: 8px;
    background: #111827;
    color: white;
    cursor: pointer;
  }

  .btn-guardar:hover { background: #1f2937; }
  .btn-guardar:disabled { opacity: 0.5; cursor: not-allowed; }

  .card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    background: white;
  }

  .seccion-titulo {
    font-size: 11px;
    font-weight: 500;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
  }

  .campo { display: flex; flex-direction: column; gap: 4px; margin-bottom: 1rem; }
  .campo:last-child { margin-bottom: 0; }

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

  .estado { text-align: center; color: #6b7280; padding: 2rem; }
  .estado.error { color: #dc2626; }
</style>