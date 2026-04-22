<script>
  import { goto } from '$app/navigation';

  const rutas = {
    verUsuarios:    '/admin/usuarios',
    verRoles:       '/admin/roles',
    verEstudiantes: '/admin/estudiantes',
    verClinicas:    '/admin/clinicas',
    verFacultad:    '/admin/facultad',
    verProgramas:   '/admin/programas',
    verReportes:    '/admin/reportes',
  };

  const modules = [
    { label: 'Usuarios',    sub: 'Gestionar cuentas',    icon: '👤', action: 'verUsuarios' },
    { label: 'Roles',       sub: 'Permisos y accesos',   icon: '🔑', action: 'verRoles' },
    { label: 'Estudiantes', sub: 'Registro estudiantil', icon: '🎓', action: 'verEstudiantes' },
    { label: 'Clínica',     sub: 'Centros de salud',     icon: '🏥', action: 'verClinicas' },
    { label: 'Facultad',    sub: 'Unidades académicas',  icon: '🏛', action: 'verFacultad' },
    { label: 'Programas',   sub: 'Programas académicos', icon: '📚', action: 'verProgramas' },
    { label: 'Reportes',    sub: 'Generar reportes PDF', icon: '📄', action: 'verReportes' },
  ];

  function handleAction(action) {
    goto(rutas[action]);
  }

  function cerrarSesion() {
    localStorage.removeItem('session');
    goto('/');
  }
</script>

<div class="admin-page">

  <button class="btn-cerrar-sesion" onclick={cerrarSesion}>
    🔒 Cerrar sesión
  </button>

  <div class="hero">
    <div class="hero-icon">🏥</div>
    <h1>Panel de Administrador</h1>
    <p class="bienvenida">Selecciona un módulo para comenzar</p>
  </div>

  <div class="grid">
    {#each modules as mod}
      <button class="card" onclick={() => handleAction(mod.action)}>
        <div class="card-icon">{mod.icon}</div>
        <div class="card-label">{mod.label}</div>
        <div class="card-sub">{mod.sub}</div>
      </button>
    {/each}
  </div>

  <footer class="footer">
    Sistema de Gestión de Enfermería &nbsp;·&nbsp; {new Date().getFullYear()}
  </footer>

</div>

<style>
  :global(body) {
    margin: 0;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
    min-height: 100vh;
  }

  .admin-page {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    box-sizing: border-box;
    position: relative;
  }

  /* ── Cerrar sesión ── */
  .btn-cerrar-sesion {
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 100;
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
    border: 1px solid rgba(220, 38, 38, 0.35);
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
  }

  .btn-cerrar-sesion:hover {
    background: rgba(220, 38, 38, 0.2);
    transform: translateY(-1px);
  }

  /* ── Hero ── */
  .hero {
    text-align: center;
    margin-bottom: 36px;
  }

  .hero-icon {
    font-size: 52px;
    margin-bottom: 10px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.12));
  }

  h1 {
    margin: 0 0 8px;
    color: #1a237e;
    font-weight: 700;
    font-size: 28px;
  }

  .bienvenida {
    margin: 0;
    color: #546e7a;
    font-size: 15px;
  }

  /* ── Grid de tarjetas ── */
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    width: 100%;
    max-width: 860px;
  }

  .card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 18px;
    padding: 34px 20px;
    cursor: pointer;
    transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
    position: relative;
    overflow: hidden;
  }

  /* Línea de acento arriba */
  .card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #1976d2, #1a237e);
    opacity: 0;
    transition: opacity 0.22s ease;
  }

  .card:hover::before {
    opacity: 1;
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.14);
    background: rgba(255, 255, 255, 0.97);
  }

  .card:active {
    transform: scale(0.97);
  }

  .card-icon {
    font-size: 42px;
    margin-bottom: 4px;
    transition: transform 0.2s;
  }

  .card:hover .card-icon {
    transform: scale(1.1);
  }

  .card-label {
    font-size: 16px;
    font-weight: 700;
    color: #1a237e;
  }

  .card-sub {
    font-size: 12.5px;
    color: #78909c;
  }

  /* ── Footer ── */
  .footer {
    margin-top: 48px;
    font-size: 12.5px;
    color: #90a4ae;
    text-align: center;
  }

  /* ── Responsive ── */
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
