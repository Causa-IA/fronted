<script>
  let { abierto, titulo, onCerrar, onGuardar, guardando = false, children } = $props();
</script>

{#if abierto}
  <div class="overlay" role="presentation">
    <div class="modal fade-in" role="dialog" aria-modal="true" aria-labelledby="modal-titulo">
      <div class="modal-header">
        <h2 id="modal-titulo">{titulo}</h2>
        <button class="btn-cerrar" onclick={onCerrar} aria-label="Cerrar modal">✕</button>
      </div>

      <div class="modal-body">
        {@render children()}
      </div>

      <div class="modal-footer">
        <button class="btn-cancelar" onclick={onCerrar}>Cancelar</button>
        <button class="btn-guardar" onclick={onGuardar} disabled={guardando}>
          {guardando ? 'Guardando...' : 'Guardar'}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 50;
  }

  .modal {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    width: 560px;
    max-width: 95vw;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.5);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #e3e8f0;
  }

  .modal-header h2 {
    font-size: 18px;
    font-weight: 700;
    color: #1a237e;
    margin: 0;
  }

  .btn-cerrar {
    background: none;
    border: none;
    font-size: 18px;
    color: #90a4ae;
    cursor: pointer;
    transition: color 0.2s;
  }

  .btn-cerrar:hover { color: #d32f2f; }

  .modal-body {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 1rem 1.5rem;
    border-top: 1px solid #e3e8f0;
  }

  .btn-cancelar {
    font-size: 14px;
    padding: 10px 20px;
    border: 1px solid #cfd8dc;
    border-radius: 10px;
    background: white;
    color: #546e7a;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  .btn-cancelar:hover {
    background: #f1f5f9;
    transform: scale(1.02);
  }

  .btn-guardar {
    font-size: 14px;
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    background: #1976d2;
    color: white;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  .btn-guardar:hover {
    background: #1565c0;
    transform: scale(1.02);
  }

  .btn-guardar:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  .fade-in {
    animation: fadeIn 0.3s ease forwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>