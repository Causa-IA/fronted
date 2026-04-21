<script>
import { goto } from '$app/navigation';
    
function cerrarSesion() {
    localStorage.removeItem('session');
    goto('/');
    }
</script>

<!-- Botón cerrar sesión - fijo arriba a la derecha -->
<button class="btn-cerrar-sesion" onclick={cerrarSesion}>
  Cerrar sesión
</button>

<style>
  /* ── Botón cerrar sesión ── */
  .btn-cerrar-sesion {
    position: fixed;
    top: 12px;
    right: 16px;
    z-index: 1100;
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
    border: 1px solid rgba(220, 38, 38, 0.4);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
  }
  .btn-cerrar-sesion:hover {
    background: rgba(220, 38, 38, 0.2);
    transform: translateY(-1px);
  }
</style>