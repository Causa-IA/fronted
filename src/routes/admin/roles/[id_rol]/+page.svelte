<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  const API = 'https://fastapi1-3jjn.onrender.com';
  const id_rol = $page.params.id_rol;

  let loading = $state(true);
  let guardando = $state(false);
  let eliminando = $state(false);
  let error = $state(null);

  let form = $state({
    id_rol: '',
    nombre: '',
    descripcion: '',
    acceso_privilegiado: false,
  });

  onMount(async () => {
    await cargarRol();
    loading = false;
  });

  async function cargarRol() {
    try {
      const res = await fetch(`${API}/roles/get_rol/${id_rol}`);
      const data = await res.json();
      form = {
        id_rol: data.id_rol,
        nombre: data.nombre,
        descripcion: data.descripcion,
        acceso_privilegiado: data.acceso_privilegiado,
      };
    } catch {
      error = 'Error al cargar el rol';
    }
  }

  async function guardar() {
    guardando = true;
    try {
      const res = await fetch(`${API}/roles/${form.id_rol}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        alert('Rol actualizado correctamente');
      } else {
        alert('Error al actualizar el rol');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  async function eliminar() {
    const confirmar = confirm('¿Estás seguro de que deseas eliminar este rol?');
    if (!confirmar) return;

    eliminando = true;
    try {
      const res = await fetch(`${API}/roles/${form.id_rol}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        goto('/admin/roles');
      } else {
        alert('Error al eliminar el rol');
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
        <button class="btn-volver" onclick={() => goto('/admin/roles')}>← Volver</button>
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
      <p class="seccion-titulo">Información del rol</p>

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

  .estado { text-align: center; color: #6b7280; padding: 2rem; }
  .estado.error { color: #dc2626; }
</style>