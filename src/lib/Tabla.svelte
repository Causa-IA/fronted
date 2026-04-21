<script>
  let {
    data = [],
    columns = [],
    onRowClick = null,
  } = $props();

  let busqueda = $state('');
  let paginaActual = $state(1);
  const porPagina = 10;

  let filtrados = $derived(
    data.filter(item =>
      columns.some(col =>
        String(item[col.key] ?? '')
          .toLowerCase()
          .includes(busqueda.toLowerCase())
      )
    )
  );

  let totalPaginas = $derived(Math.ceil(filtrados.length / porPagina));

  let paginados = $derived(
    filtrados.slice((paginaActual - 1) * porPagina, paginaActual * porPagina)
  );

  $effect(() => {
    busqueda;
    paginaActual = 1;
  });
</script>

<div class="tabla-wrapper fade-in">
  <div class="tabla-top">
    <span class="tabla-count">{filtrados.length} registros encontrados</span>
    <div class="search-box">
      <input
        type="text"
        placeholder="Buscar..."
        bind:value={busqueda}
      />
    </div>
  </div>

  {#if filtrados.length === 0}
    <p class="no-results">❌ No se encontraron resultados</p>
  {:else}
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            {#each columns as col}
              <th>{col.label}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each paginados as item}
            <tr
              onclick={() => onRowClick?.(item)}
              class:clickable={onRowClick}
            >
              {#each columns as col}
                <td>
                  {#if col.key === 'estado'}
                    <span class="dot {String(item[col.key]) === 'true' ? 'activo' : 'inactivo'}"></span>
                  {:else}
                    {item[col.key] ?? '—'}
                  {/if}
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <span class="pag-info">
        Mostrando {(paginaActual - 1) * porPagina + 1}–{Math.min(paginaActual * porPagina, filtrados.length)} de {filtrados.length}
      </span>
      <div class="pag-btns">
        <button
          class="pag-btn"
          disabled={paginaActual === 1}
          onclick={() => paginaActual--}
        >←</button>

        {#each Array.from({ length: totalPaginas }, (_, i) => i + 1) as num}
          <button
            class="pag-btn"
            class:active={num === paginaActual}
            onclick={() => paginaActual = num}
          >{num}</button>
        {/each}

        <button
          class="pag-btn"
          disabled={paginaActual === totalPaginas}
          onclick={() => paginaActual++}
        >→</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .tabla-wrapper { width: 100%; }

  .tabla-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .tabla-count {
    font-size: 14px;
    font-weight: 600;
    color: #546e7a;
  }

  .search-box input {
    width: 260px;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #cfd8dc;
    background: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    transition: all 0.3s ease;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  .search-box input:focus {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2);
  }

  .table-wrap {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;  
  }

  table {
    width: 100%;
    border-collapse: collapse;
    background: white;
  }

  thead {
    background: #0f172a;
    color: white;
  }

  th {
    padding: 14px 12px;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
  }

  td {
    padding: 12px;
    text-align: left;
    font-size: 14px;
    border-bottom: 1px solid #f1f5f9;
    color: #34495e;
  }

  tbody tr:last-child td { border-bottom: none; }

  tbody tr.clickable {
    cursor: pointer;
    transition: background 0.2s ease;
  }

  tbody tr.clickable:hover { background: #f1f5f9; }

  .dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .dot.activo  { background: #16a34a; }
  .dot.inactivo { background: #dc2626; }

  .pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0 0;
  }

  .pag-info {
    font-size: 13px;
    color: #546e7a;
    font-weight: 600;
  }

  .pag-btns { display: flex; gap: 6px; }

  .pag-btn {
    font-size: 13px;
    padding: 6px 12px;
    border: 1px solid #cfd8dc;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.8);
    color: #34495e;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
  }

  .pag-btn:hover:not(:disabled) {
    background: #1976d2;
    color: white;
    border-color: #1976d2;
    transform: scale(1.05);
  }

  .pag-btn:disabled { opacity: 0.4; cursor: not-allowed; }

  .pag-btn.active {
    background: #1976d2;
    color: white;
    border-color: #1976d2;
  }

  .no-results {
    text-align: center;
    margin-top: 20px;
    font-size: 15px;
    color: #d32f2f;
    font-weight: 600;
  }

  .fade-in {
    animation: fadeIn 0.6s ease forwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>