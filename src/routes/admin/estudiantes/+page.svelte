<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Tabla from '$lib/Tabla.svelte';
  import Modal from '$lib/Modal.svelte';

  const API = 'https://fastapi1-3jjn.onrender.com';

  let estudiantes = $state([]);
  let facultades = $state([]);
  let programas = $state([]);
  let usuarios = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let modalAbierto = $state(false);
  let guardando = $state(false);

  let form = $state({
    primer_nombre: '',
    primer_apellido: '',
    tipo_identificacion: 'CC',
    numero_identificacion: '',
    genero: '',
    telefono: '',
    direccion: '',
    id_facultad: '',
    id_programa: '',
    id_usuario: '',
  });

  onMount(async () => {
    await Promise.all([
      cargarEstudiantes(),
      cargarFacultades(),
      cargarProgramas(),
      cargarUsuarios(),
    ]);
    loading = false;
  });

  async function cargarEstudiantes() {
    try {
      const res = await fetch(`${API}/estudiantes/get_estudiantes/`);
      const data = await res.json();
      estudiantes = data.resultado ?? [];
    } catch {
      error = 'Error al cargar estudiantes';
    }
  }

  async function cargarFacultades() {
    const res = await fetch(`${API}/facultades/get_facultades/`);
    const data = await res.json();
    facultades = data.resultado ?? [];
  }

  async function cargarProgramas() {
    const res = await fetch(`${API}/programas/get_programas/`);
    const data = await res.json();
    programas = data.resultado ?? [];
  }

  async function cargarUsuarios() {
    const res = await fetch(`${API}/usuarios/get_usuarios/`);
    const data = await res.json();
    usuarios = data.resultado ?? [];
  }

  function abrirModal() {
    form = {
      primer_nombre: '',
      primer_apellido: '',
      tipo_identificacion: 'CC',
      numero_identificacion: '',
      genero: '',
      telefono: '',
      direccion: '',
      id_facultad: '',
      id_programa: '',
      id_usuario: '',
    };
    modalAbierto = true;
  }

  async function crearEstudiante() {
    guardando = true;
    try {
      const res = await fetch(`${API}/estudiantes/create_estudiante`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          numero_identificacion: Number(form.numero_identificacion),
          telefono: Number(form.telefono),
          id_facultad: Number(form.id_facultad),
          id_programa: Number(form.id_programa),
          id_usuario: Number(form.id_usuario),
        }),
      });

      if (res.ok) {
        await cargarEstudiantes();
        modalAbierto = false;
      } else {
        alert('Error al crear el estudiante');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  const columnas = [
    { label: 'Nombre',         key: 'primer_nombre' },
    { label: 'Apellido',       key: 'primer_apellido' },
    { label: 'Identificación', key: 'numero_identificacion' },
    { label: 'Tipo ID',        key: 'tipo_identificacion' },
    { label: 'Género',         key: 'genero' },
    { label: 'Teléfono',       key: 'telefono' },
    { label: 'Dirección',      key: 'direccion' },
  ];
</script>

<div class="page">
  <div class="top">
    <button class="btn-volver" onclick={() => goto('/admin')}>← Volver</button>
    <h2>Estudiantes</h2>
    <button class="btn-agregar" onclick={abrirModal}>+ Agregar estudiante</button>
  </div>

  {#if loading}
    <p class="estado">Cargando...</p>
  {:else if error}
    <p class="estado error">{error}</p>
  {:else}
    <Tabla
      data={estudiantes}
      columns={columnas}
      onRowClick={(item) => goto(`/admin/estudiantes/${item.numero_identificacion}`)}
    />
  {/if}
</div>

<Modal
  abierto={modalAbierto}
  titulo="Agregar estudiante"
  onCerrar={() => modalAbierto = false}
  onGuardar={crearEstudiante}
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
      <label for="tipo_id">Tipo de identificación</label>
      <select id="tipo_id" bind:value={form.tipo_identificacion}>
        <option value="CC">CC</option>
        <option value="TI">TI</option>
        <option value="CE">CE</option>
        <option value="PA">PA</option>
      </select>
    </div>
    <div class="campo">
      <label for="numero_id">Número de identificación</label>
      <input id="numero_id" type="number" bind:value={form.numero_identificacion} />
    </div>
  </div>

  <div class="fila">
    <div class="campo">
      <label for="genero">Género</label>
      <select id="genero" bind:value={form.genero}>
        <option value="Masculino">Masculino</option>
        <option value="Femenino">Femenino</option>
        <option value="Otro">Otro</option>
      </select>
    </div>
    <div class="campo">
      <label for="telefono">Teléfono</label>
      <input id="telefono" type="number" bind:value={form.telefono} />
    </div>
  </div>

  <div class="campo">
    <label for="direccion">Dirección</label>
    <input id="direccion" type="text" bind:value={form.direccion} />
  </div>

  <div class="fila">
    <div class="campo">
      <label for="facultad">Facultad</label>
      <select id="facultad" bind:value={form.id_facultad}>
        <option value="">Seleccionar...</option>
        {#each facultades as f}
          <option value={f.id_facultad}>{f.nombre}</option>
        {/each}
      </select>
    </div>
    <div class="campo">
      <label for="programa">Programa</label>
      <select id="programa" bind:value={form.id_programa}>
        <option value="">Seleccionar...</option>
        {#each programas as p}
          <option value={p.id_programa}>{p.nombre}</option>
        {/each}
      </select>
    </div>
  </div>

  <div class="campo">
    <label for="usuario">Usuario</label>
    <select id="usuario" bind:value={form.id_usuario}>
      <option value="">Seleccionar...</option>
      {#each usuarios as u}
        <option value={u.id_usuario}>{u.primer_nombre} {u.primer_apellido}</option>
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
</style>