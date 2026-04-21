<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  const API = 'https://fastapi1-3jjn.onrender.com';

  const numero_identificacion = $page.params.numero_identificacion;

  let estudiante = $state(null);
  let facultades = $state([]);
  let programas = $state([]);
  let loading = $state(true);
  let guardando = $state(false);
  let eliminando = $state(false);
  let error = $state(null);

  let form = $state({
    primer_nombre: '',
    primer_apellido: '',
    tipo_identificacion: '',
    numero_identificacion: '',
    genero: '',
    telefono: '',
    direccion: '',
    id_facultad: '',
    id_programa: '',
    id_usuario: '',
    fecha_registro: '',
    id_estudiante: '',
  });

  onMount(async () => {
    await Promise.all([
      cargarEstudiante(),
      cargarFacultades(),
      cargarProgramas(),
    ]);
    loading = false;
  });

  async function cargarEstudiante() {
    try {
      const res = await fetch(`${API}/estudiantes/get_estudiante/${numero_identificacion}`);
      const data = await res.json();
      estudiante = data;
      form = {
        primer_nombre: data.primer_nombre,
        primer_apellido: data.primer_apellido,
        tipo_identificacion: data.tipo_identificacion,
        numero_identificacion: data.numero_identificacion,
        genero: data.genero,
        telefono: data.telefono,
        direccion: data.direccion,
        id_facultad: data.id_facultad,
        id_programa: data.id_programa,
        id_usuario: data.id_usuario,
        fecha_registro: data.fecha_registro,
        id_estudiante: data.id_estudiante,
      };
    } catch {
      error = 'Error al cargar el estudiante';
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

  async function guardar() {
    guardando = true;
    try {
      const res = await fetch(`${API}/estudiantes/${form.id_estudiante}`, {
        method: 'PUT',
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
        alert('Estudiante actualizado correctamente');
        goto('/admin/estudiantes');
      } else {
        alert('Error al actualizar el estudiante');
      }
    } catch {
      alert('Error de conexión');
    } finally {
      guardando = false;
    }
  }

  async function eliminar() {
    const confirmar = confirm('¿Estás seguro de que deseas eliminar este estudiante?');
    if (!confirmar) return;

    eliminando = true;
    try {
      const res = await fetch(`${API}/estudiantes/${form.id_estudiante}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        goto('/admin/estudiantes');
      } else {
        alert('Error al eliminar el estudiante');
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
        <button class="btn-volver" onclick={() => goto('/admin/estudiantes')}>← Volver</button>
        <h2>{form.primer_nombre} {form.primer_apellido}</h2>
        <p class="sub">CC {form.numero_identificacion}</p>
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
    </div>

    <div class="card">
      <p class="seccion-titulo">Información académica</p>
      <div class="fila">
        <div class="campo">
          <label for="facultad">Facultad</label>
          <select id="facultad" bind:value={form.id_facultad}>
            {#each facultades as f}
              <option value={f.id_facultad}>{f.nombre}</option>
            {/each}
          </select>
        </div>
        <div class="campo">
          <label for="programa">Programa</label>
          <select id="programa" bind:value={form.id_programa}>
            {#each programas as p}
              <option value={p.id_programa}>{p.nombre}</option>
            {/each}
          </select>
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

  .estado { text-align: center; color: #6b7280; padding: 2rem; }
  .estado.error { color: #dc2626; }
</style>