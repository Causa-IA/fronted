<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  const API = 'https://fastapi1-3jjn.onrender.com';

  const id_usuario = $page.params.id_usuario;

  let roles = $state([]);
  let loading = $state(true);
  let guardando = $state(false);
  let eliminando = $state(false);
  let error = $state(null);

  let form = $state({
    id_usuario: '',
    primer_nombre: '',
    primer_apellido: '',
    telefono: '',
    email: '',
    password: '',
    estado: true,
    id_rol: '',
  });

  onMount(async () => {
    await Promise.all([cargarUsuario(), cargarRoles()]);
    loading = false;
  });

  async function cargarUsuario() {
    try {
      const res = await fetch(`${API}/usuarios/get_usuario/${id_usuario}`);
      const data = await res.json();
      form = {
        id_usuario: data.id_usuario,
        primer_nombre: data.primer_nombre,
        primer_apellido: data.primer_apellido,
        telefono: data.telefono,
        email: data.email,
        password: data.password,
        estado: data.estado,
        id_rol: data.id_rol,
      };
    } catch {
      error = 'Error al cargar el usuario';
    }
  }

  async function cargarRoles() {
    const res = await fetch(`${API}/roles/get_roles/`);
    const data = await res.json();
    roles = data.resultado ?? [];
  }

  async function guardar() {
    guardando = true;
    try {
      const res = await fetch(`${API}/usuarios/${form.id_usuario}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          id_rol: Number(form.id_rol),
        }),
      });

      if (res.ok) {
        alert('Usuario actualizado correctamente');
        goto('/admin/usuarios');
      } else {
        alert('Error al actualizar el usuario');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  async function eliminar() {
    const confirmar = confirm('¿Estás seguro de que deseas eliminar este usuario?');
    if (!confirmar) return;

    eliminando = true;
    try {
      const res = await fetch(`${API}/usuarios/${form.id_usuario}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        goto('/admin/usuarios');
      } else {
        alert('Error al eliminar el usuario');
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
        <button class="btn-volver" onclick={() => goto('/admin/usuarios')}>← Volver</button>
        <h2>{form.primer_nombre} {form.primer_apellido}</h2>
        <p class="sub">{form.email}</p>
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
      <p class="seccion-titulo">Información personal</p>
      <div class="fila">
        <div class="campo">
          <label for="primer_nombre">Primer nombre</label>
          <input id="primer_nombre" type="text" bind:value={form.primer_nombre} />
        </div>
        <div class="campo">
          <label for="primer_apellido">Primer apellido</label>
          <input id="primer_apellido" type="text" bind:value={form.primer_apellido} />
        </div>
      </div>

      <div class="fila">
        <div class="campo">
          <label for="telefono">Teléfono</label>
          <input id="telefono" type="text" bind:value={form.telefono} />
        </div>
        <div class="campo">
          <label for="email">Email</label>
          <input id="email" type="email" bind:value={form.email} />
        </div>
      </div>

      <div class="campo">
        <label for="password">Contraseña</label>
        <input id="password" type="password" bind:value={form.password} />
      </div>
    </div>

    <div class="card">
      <p class="seccion-titulo">Acceso y permisos</p>
      <div class="fila">
        <div class="campo">
          <label for="rol">Rol</label>
          <select id="rol" bind:value={form.id_rol}>
            {#each roles as r}
              <option value={r.id_rol}>{r.nombre}</option>
            {/each}
          </select>
        </div>
        <div class="campo-toggle">
  <span class="toggle-label">Estado</span>
  <button
    class="toggle {form.estado ? 'activo' : 'inactivo'}"
    onclick={() => form.estado = !form.estado}
    type="button"
  >
    <span class="toggle-thumb"></span>
    <span class="toggle-text">{form.estado ? 'Activo' : 'Inactivo'}</span>
  </button>
</div>
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

  .fila { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }

  .campo { display: flex; flex-direction: column; gap: 4px; margin-bottom: 1rem; }
  .campo:last-child { margin-bottom: 0; }

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

  .campo-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toggle-label {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
}

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

.toggle.activo .toggle-thumb {
  background: #16a34a;
}

.toggle.activo .toggle-thumb::after {
  left: 19px;
}

.toggle.inactivo .toggle-thumb {
  background: #d1d5db;
}

.toggle.inactivo .toggle-thumb::after {
  left: 3px;
}

.toggle.activo { color: #16a34a; border-color: #bbf7d0; }
.toggle.inactivo { color: #6b7280; border-color: #e5e7eb; }

  .estado { text-align: center; color: #6b7280; padding: 2rem; }
  .estado.error { color: #dc2626; }
</style>