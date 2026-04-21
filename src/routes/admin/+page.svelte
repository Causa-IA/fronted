<script>
  import { goto } from '$app/navigation';
  import CerrarSesion from '$lib/CerrarSesion.svelte';

  const rutas = {
    verUsuarios:    '/admin/usuarios',
    verRoles:       '/admin/roles',
    verEstudiantes: '/admin/estudiantes',
    verClinicas:     '/admin/clinicas',
    verFacultad:    '/admin/facultad',
    verProgramas:    '/admin/programas',
  };

  const modules = [
    { label: 'Usuarios',     sub: 'Gestionar cuentas',    icon: '👤', action: 'verUsuarios' },
    { label: 'Roles',        sub: 'Permisos y accesos',   icon: '🔑', action: 'verRoles' },
    { label: 'Estudiantes',  sub: 'Registro estudiantil', icon: '🎓', action: 'verEstudiantes' },
    { label: 'Clínica',      sub: 'Centros de salud',     icon: '🏥', action: 'verClinicas' },
    { label: 'Facultad',     sub: 'Unidades académicas',  icon: '🏛', action: 'verFacultad' },
    { label: 'Programas',    sub: 'Programas académicos', icon: '📚', action: 'verProgramas' },
  ];

  function handleAction(action) {
    goto(rutas[action]);
  }
</script>

<div class="admin-page">


    <h1>Panel de Administrador</h1>
    <p class="bienvenida">Selecciona un módulo para comenzar</p>

    <div class="grid">
      {#each modules as mod}
        <button class="card" onclick={() => handleAction(mod.action)}>
          <div class="card-icon">{mod.icon}</div>
          <div class="card-label">{mod.label}</div>
          <div class="card-sub">{mod.sub}</div>
        </button>
      {/each}
    </div>
  </div>

<style>
  :global(body) {
    margin: 0;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }

  .admin-page {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px 40px;
  }

  h1 {
    text-align: center;
    margin: 0 0 8px;
    color: #1a237e;
    font-weight: 700;
    font-size: 28px;
  }

  .bienvenida {
    text-align: center;
    color: #546e7a;
    font-size: 15px;
    margin: 0 0 40px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }

  .card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 16px;
    padding: 32px 20px;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
    background: rgba(255, 255, 255, 0.95);
  }

  .card:active {
    transform: scale(0.98);
  }

  .card-icon {
    font-size: 40px;
    margin-bottom: 4px;
  }

  .card-label {
    font-size: 17px;
    font-weight: 700;
    color: #1a237e;
  }

  .card-sub {
    font-size: 13px;
    color: #78909c;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }

@media (max-width: 600px) {
  .grid {
    grid-template-columns: 1fr;
  }

}

@media (min-width: 601px) and (max-width: 850px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

</style>