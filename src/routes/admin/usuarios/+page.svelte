<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '../../../lib/Tabla.svelte';
  import Modal from '../../../lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let usuarios = $state([]);
  let roles = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    primer_nombre: '',
    primer_apellido: '',
    telefono: '',
    email: '',
    password: '',
    estado: true,
    id_rol: '',
  });

  onMount(async () => {
    await Promise.all([cargarUsuarios(), cargarRoles()]);
    usuarios = cruzarRoles(usuarios, roles);
    loading = false;
  });

  async function cargarUsuarios() {
    try {
      const res = await fetch(`${API}/usuarios/get_usuarios/`);
      const data = await res.json();
      usuarios = data.resultado ?? [];
    } catch {
      error = 'Error al cargar usuarios';
    }
  }

  async function cargarRoles() {
    const res = await fetch(`${API}/roles/get_roles/`);
    const data = await res.json();
    roles = data.resultado ?? [];
  }

  function abrirModal() {
    form = {
      primer_nombre: '',
      primer_apellido: '',
      telefono: '',
      email: '',
      password: '',
      estado: true,
      id_rol: '',
    };
    modalAbierto = true;
  }

  async function crearUsuario() {
    guardando = true;
    try {
      const res = await fetch(`${API}/usuarios/create_usuario`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          id_rol: Number(form.id_rol),
        }),
      });

      if (res.ok) {
        await cargarUsuarios();
        modalAbierto = false;
      } else {
        alert('Error al crear el usuario');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  const columnas = [
    { label: 'Nombre',   key: 'primer_nombre' },
    { label: 'Apellido', key: 'primer_apellido' },
    { label: 'Teléfono', key: 'telefono' },
    { label: 'Email',    key: 'email' },
    { label: 'Estado',   key: 'estado' },
    { label: 'Rol',      key: 'nombre_rol' },
  ];

  function cruzarRoles(usuarios, roles) {
  return usuarios.map(u => ({
      ...u,
      nombre_rol: roles.find(r => r.id_rol === u.id_rol)?.nombre ?? '—'
    }));
  }
</script>

<div class="page">
  <div class="top">
  <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Usuarios</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar usuario</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={usuarios}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/usuarios/${item.id_usuario}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar usuario"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearUsuario}
  {guardando}
>
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

  <div class="fila">
    <div class="campo">
      <label for="password">Contraseña</label>
      <input id="password" type="password" bind:value={form.password} />
    </div>
    <div class="campo">
      <label for="rol">Rol</label>
      <select id="rol" bind:value={form.id_rol}>
        <option value="">Seleccionar...</option>
        {#each roles as r}
          <option value={r.id_rol}>{r.nombre}</option>
        {/each}
      </select>
    </div>
  </div>

  <div class="campo-check">
    <input id="estado" type="checkbox" bind:checked={form.estado} />
    <label for="estado">Usuario activo</label>
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

  .fila { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

  .campo { display: flex; flex-direction: column; gap: 4px; }

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

  .campo-check {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #374151;
  }
</style>