<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  const API_URL = 'https://fastapi1-3jjn.onrender.com';

  // ── Filtros ──
  let filtroNombre     = '';
  let filtroFechaDesde = '';
  let filtroFechaHasta = '';
  let filtroEnfermera  = '';

  // ── Datos ──
  let consultas    = [];
  let filtradas    = [];
  let enfermeras   = [];
  let loading      = false;
  let generando    = false;

  onMount(async () => {
    if (!browser) return;
    await cargarDatos();
  });


  async function notificarReporte() {
    try {
      await fetch(`${API_URL}/email/reporte_generado`, { method: 'POST' });
    } catch {
      console.error('Error al enviar el email');
    }
  }

  async function cargarDatos() {
    loading = true;
    try {
      const res  = await fetch(`${API_URL}/consultas/get_consultas/`);
      const data = await res.json();
      consultas = data.resultado || [];
      filtradas = [...consultas];

      // Extraer enfermeras únicas para el filtro
      const nombres = [...new Set(consultas.map(c => c.nombre_enfermera).filter(Boolean))];
      enfermeras = nombres;
    } catch (e) {
      console.error('Error cargando consultas:', e);
    } finally {
      loading = false;
    }
  }

  function aplicarFiltros() {
    filtradas = consultas.filter(c => {
      const nombre  = filtroNombre.toLowerCase();
      const matchNombre = !filtroNombre ||
        (c.nombre_estudiante || '').toLowerCase().includes(nombre) ||
        (c.cedula || '').includes(filtroNombre);

      const fecha = c.fecha_entrada ? new Date(c.fecha_entrada) : null;
      const matchDesde = !filtroFechaDesde || (fecha && fecha >= new Date(filtroFechaDesde));
      const matchHasta = !filtroFechaHasta || (fecha && fecha <= new Date(filtroFechaHasta + 'T23:59:59'));
      const matchEnfermera = !filtroEnfermera || c.nombre_enfermera === filtroEnfermera;

      return matchNombre && matchDesde && matchHasta && matchEnfermera;
    });
  }

  function limpiarFiltros() {
    filtroNombre     = '';
    filtroFechaDesde = '';
    filtroFechaHasta = '';
    filtroEnfermera  = '';
    filtradas = [...consultas];
  }

  function formatFecha(f) {
    if (!f) return '—';
    return new Date(f).toLocaleDateString('es-CO', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  async function generarPDF() {
    if (filtradas.length === 0) return;
    generando = true;

    try {
      const { jsPDF }     = await import('jspdf');
      const { default: autoTable } = await import('jspdf-autotable');

      const doc  = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
      const W    = doc.internal.pageSize.getWidth();
      const H    = doc.internal.pageSize.getHeight();
      const hoy  = new Date().toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric' });

      // ── Paleta ──
      const AZUL_OSCURO  = [26,  35, 126];   // #1a237e
      const AZUL_MEDIO   = [25, 118, 210];   // #1976d2
      const AZUL_CLARO   = [227, 242, 253];  // #e3f2fd
      const GRIS_TEXTO   = [55,  71,  79];
      const BLANCO       = [255, 255, 255];
      const VERDE        = [46, 125,  50];
      const ROJO         = [198,  40,  40];

      const totalPages = () => doc.internal.getNumberOfPages();

      // ════════════════════════════════════════
      //  Función encabezado (se llama por página)
      // ════════════════════════════════════════
      function dibujarEncabezado() {
        // Barra superior azul oscuro
        doc.setFillColor(...AZUL_OSCURO);
        doc.rect(0, 0, W, 22, 'F');

        // Título institución
        doc.setTextColor(...BLANCO);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(13);
        doc.text('SISTEMA DE GESTIÓN DE ENFERMERÍA', W / 2, 9, { align: 'center' });

        // Subtítulo
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(9);
        doc.text('Reporte de Consultas Médicas Escolares', W / 2, 16, { align: 'center' });

        // Línea decorativa azul medio
        doc.setFillColor(...AZUL_MEDIO);
        doc.rect(0, 22, W, 2, 'F');

        // Info del reporte
        doc.setTextColor(...GRIS_TEXTO);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8);
        doc.text(`Fecha de generación: ${hoy}`, 14, 30);
        doc.text(`Total de registros: ${filtradas.length}`, 14, 36);

        // Filtros aplicados
        const filtrosAplicados = [];
        if (filtroNombre)     filtrosAplicados.push(`Búsqueda: "${filtroNombre}"`);
        if (filtroEnfermera)  filtrosAplicados.push(`Enfermera: ${filtroEnfermera}`);
        if (filtroFechaDesde) filtrosAplicados.push(`Desde: ${filtroFechaDesde}`);
        if (filtroFechaHasta) filtrosAplicados.push(`Hasta: ${filtroFechaHasta}`);

        if (filtrosAplicados.length > 0) {
          doc.text(`Filtros: ${filtrosAplicados.join('  |  ')}`, 14, 42);
        }
      }

      // ════════════════════════════════════════
      //  Función pie de página
      // ════════════════════════════════════════
      function dibujarPiePagina(pageNum, total) {
        // Línea separadora
        doc.setDrawColor(...AZUL_MEDIO);
        doc.setLineWidth(0.5);
        doc.line(14, H - 14, W - 14, H - 14);

        // Texto pie
        doc.setTextColor(...GRIS_TEXTO);
        doc.setFont('helvetica', 'italic');
        doc.setFontSize(7.5);
        doc.text('Documento generado automáticamente — Sistema de Enfermería Escolar', 14, H - 8);
        doc.text(`Página ${pageNum} de ${total}`, W - 14, H - 8, { align: 'right' });

        // Rectángulo decorativo pie
        doc.setFillColor(...AZUL_OSCURO);
        doc.rect(0, H - 4, W, 4, 'F');
      }

      // ── Primera página: encabezado + resumen estadístico ──
      dibujarEncabezado();

      // Tarjetas de resumen
      const stats = [
        { label: 'Total consultas',  valor: filtradas.length,                          color: AZUL_MEDIO },
        { label: 'Estudiantes únicos', valor: new Set(filtradas.map(c => c.cedula)).size, color: VERDE },
        { label: 'Enfermeras',       valor: new Set(filtradas.map(c => c.nombre_enfermera)).size, color: [106, 27, 154] },
        { label: 'Con emergencia',   valor: filtradas.filter(c => c.es_emergencia).length, color: ROJO },
      ];

      const cardW = (W - 28 - 12) / 4;
      stats.forEach((s, i) => {
        const x = 14 + i * (cardW + 4);
        doc.setFillColor(...s.color);
        doc.roundedRect(x, 48, cardW, 22, 3, 3, 'F');
        doc.setTextColor(...BLANCO);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(18);
        doc.text(String(s.valor), x + cardW / 2, 60, { align: 'center' });
        doc.setFontSize(7.5);
        doc.setFont('helvetica', 'normal');
        doc.text(s.label, x + cardW / 2, 66, { align: 'center' });
      });

      // ── Tabla principal ──
      const filas = filtradas.map(c => [
        c.nombre_estudiante || '—',
        c.cedula            || '—',
        c.nombre_enfermera  || '—',
        c.motivo_consulta   || '—',
        c.diagnostico       || '—',
        formatFecha(c.fecha_entrada),
        formatFecha(c.fecha_salida),
      ]);

      autoTable(doc, {
        startY: 76,
        head: [['Estudiante', 'Cédula', 'Enfermera', 'Motivo', 'Diagnóstico', 'Entrada', 'Salida']],
        body: filas,
        theme: 'grid',
        styles: {
          fontSize: 8,
          cellPadding: 3,
          textColor: GRIS_TEXTO,
          lineColor: [200, 210, 220],
          lineWidth: 0.3,
          overflow: 'linebreak',
        },
        headStyles: {
          fillColor: AZUL_MEDIO,
          textColor: BLANCO,
          fontStyle: 'bold',
          fontSize: 8.5,
          halign: 'center',
        },
        alternateRowStyles: {
          fillColor: AZUL_CLARO,
        },
        columnStyles: {
          0: { cellWidth: 38 },
          1: { cellWidth: 24, halign: 'center' },
          2: { cellWidth: 36 },
          3: { cellWidth: 44 },
          4: { cellWidth: 44 },
          5: { cellWidth: 32, halign: 'center' },
          6: { cellWidth: 32, halign: 'center' },
        },
        didDrawPage: (hookData) => {
          // Encabezado en páginas 2+
          if (hookData.pageNumber > 1) {
            dibujarEncabezado();
          }
        },
        margin: { top: 76, left: 14, right: 14, bottom: 20 },
      });

      // ── Pie de página en todas las páginas ──
      const total = totalPages();
      for (let i = 1; i <= total; i++) {
        doc.setPage(i);
        dibujarPiePagina(i, total);
      }
      await notificarReporte();
      // ── Descargar ──
      const nombreArchivo = `reporte_consultas_${new Date().toISOString().slice(0, 10)}.pdf`;
      doc.save(nombreArchivo);

    } catch (e) {
      console.error('Error generando PDF:', e);
      alert('Error al generar el PDF. Verifica la consola.');
    } finally {
      generando = false;
    }
  }

  function volver() {
    window.location.href = '/admin';
  }
</script>


<div class="page">

  <div class="container">

    <div class="header-row">
      <div>
        <h1>📄 Reportes</h1>
        <p class="sub">Filtra las consultas y genera un PDF con los resultados</p>
      </div>
      <button class="btn-volver" onclick={volver}>⬅ Volver</button>
    </div>

    <!-- Filtros -->
    <div class="filtros">
      <div class="filtro-item">
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label>Estudiante o cédula</label>
        <input type="text" placeholder="Nombre o cédula..." bind:value={filtroNombre} />
      </div>
      <div class="filtro-item">
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label>Enfermera</label>
        <select bind:value={filtroEnfermera}>
          <option value="">Todas</option>
          {#each enfermeras as e}
            <option value={e}>{e}</option>
          {/each}
        </select>
      </div>
      <div class="filtro-item">
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label>Fecha desde</label>
        <input type="date" bind:value={filtroFechaDesde} />
      </div>
      <div class="filtro-item">
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label>Fecha hasta</label>
        <input type="date" bind:value={filtroFechaHasta} />
      </div>
    </div>

    <div class="acciones">
      <button class="btn-filtrar" onclick={aplicarFiltros}>🔍 Aplicar filtros</button>
      <button class="btn-limpiar" onclick={limpiarFiltros}>✖ Limpiar</button>
      <button
        class="btn-pdf"
        onclick={generarPDF}
        disabled={filtradas.length === 0 || generando}
      >
        {generando ? '⏳ Generando...' : `📥 Descargar PDF (${filtradas.length})`}
      </button>
    </div>

    <!-- Tabla preview -->
    {#if loading}
      <div class="center"><div class="spinner"></div><p>Cargando...</p></div>

    {:else if filtradas.length === 0}
      <p class="no-results">❌ No hay consultas con esos filtros</p>

    {:else}
      <div class="tabla-wrapper">
        <table>
          <thead>
            <tr>
              <th>Estudiante</th>
              <th>Cédula</th>
              <th>Enfermera</th>
              <th>Motivo</th>
              <th>Diagnóstico</th>
              <th>Entrada</th>
              <th>Salida</th>
            </tr>
          </thead>
          <tbody>
            {#each filtradas as c}
              <tr>
                <td>{c.nombre_estudiante || '—'}</td>
                <td>{c.cedula || '—'}</td>
                <td>{c.nombre_enfermera || '—'}</td>
                <td>{c.motivo_consulta || '—'}</td>
                <td>{c.diagnostico || '—'}</td>
                <td>{formatFecha(c.fecha_entrada)}</td>
                <td>{formatFecha(c.fecha_salida)}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  </div>
</div>


<style>
  :global(body) {
    margin: 0;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
    min-height: 100vh;
  }

  .page {
    display: flex;
    justify-content: center;
    padding: 40px 20px;
  }

  .container {
    width: 100%;
    max-width: 1100px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.25);
  }

  .header-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
  }

  h1 {
    margin: 0;
    color: #1a237e;
    font-size: 26px;
  }

  .sub {
    margin: 4px 0 0;
    color: #546e7a;
    font-size: 14px;
  }

  /* Filtros */
  .filtros {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.07);
    margin-bottom: 16px;
  }

  .filtro-item label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: #546e7a;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .filtro-item input,
  .filtro-item select {
    width: 100%;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid #dcdfe6;
    font-size: 14px;
    transition: all 0.2s;
    box-sizing: border-box;
  }

  .filtro-item input:focus,
  .filtro-item select:focus {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.15);
  }

  /* Botones de acción */
  .acciones {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
  }

  .btn-filtrar, .btn-limpiar, .btn-pdf, .btn-volver {
    padding: 10px 22px;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, filter 0.2s;
  }

  .btn-filtrar {
    background: #1976d2;
    color: white;
  }

  .btn-limpiar {
    background: #eceff1;
    color: #546e7a;
  }

  .btn-pdf {
    background: #1a237e;
    color: white;
    margin-left: auto;
  }

  .btn-volver {
    background: rgba(255,255,255,0.6);
    color: #1a237e;
    border: 1px solid rgba(26, 35, 126, 0.3);
  }

  .btn-filtrar:hover, .btn-limpiar:hover,
  .btn-pdf:hover, .btn-volver:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
  }

  .btn-pdf:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  /* Tabla */
  .tabla-wrapper {
    overflow-x: auto;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    font-size: 13.5px;
  }

  thead {
    background: #1a237e;
    color: white;
  }

  th {
    padding: 12px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
  }

  td {
    padding: 11px 14px;
    color: #37474f;
    border-bottom: 1px solid #eceff1;
  }

  tbody tr:nth-child(even) {
    background: #e3f2fd;
  }

  tbody tr:hover {
    background: #bbdefb;
    transition: background 0.15s;
  }

  .no-results {
    text-align: center;
    color: #d32f2f;
    font-weight: 600;
    margin-top: 30px;
  }

  /* Loading */
  .center {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    color: #90a4ae;
  }

  .spinner {
    width: 36px;
    height: 36px;
    border: 3px solid rgba(25, 118, 210, 0.2);
    border-top-color: #1976d2;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 12px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }
</style>
