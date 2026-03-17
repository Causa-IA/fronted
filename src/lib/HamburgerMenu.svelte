<script>
  let menuAbierto = false;
  function toggleMenu() {
    menuAbierto = !menuAbierto;
  }
</script>

<button 
  class="hamburger" 
  on:click={toggleMenu} 
  aria-label="Abrir menú" 
  aria-expanded={menuAbierto}
>
  <span class:active={menuAbierto}></span>
  <span class:active={menuAbierto}></span>
  <span class:active={menuAbierto}></span>
</button>

{#if menuAbierto}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="menu-overlay" on:click={toggleMenu}></div>
  <nav class="menu slide-in">
    <a href="/search_student">🔎 Buscar estudiante</a>
    <a href="/consultas_list">📋 Ver consultas</a>
  </nav>
{/if}

<style>
.hamburger {
  position: fixed;
  top: 15px;
  left: 15px;   
  width: 30px;  
  height: 24px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1100;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.hamburger span {
  height: 3px;
  width: 36px;          
  background: #1e3a5f;  
  border-radius: 2px;
  transition: all 0.3s ease;
  align-self: center;   
}


.hamburger span.active:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}
.hamburger span.active:nth-child(2) {
  opacity: 0;
}
.hamburger span.active:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

.menu-overlay {
  position: fixed;
  top:0; left:0;
  width:100%; height:100%;
  background: rgba(0,0,0,0.4);
  z-index: 1000;
  animation: fadeIn 0.3s ease forwards;
}


.menu {
  position: fixed;
  top:0; left:0;
  width: 260px;
  height: 100vh;
  background: white;
  padding-top: 80px;
  box-shadow: 4px 0 10px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1050;
}

.menu a {
  padding: 15px 25px;
  text-decoration: none;
  color: #1e3a5f;
  font-weight: 600;
  border-left: 4px solid transparent;
  transition: 0.2s;
}

.menu a:hover {
  background: #f2f6fb;
  border-left: 4px solid #1e3a5f;
}


.slide-in { animation: slideIn 0.3s ease forwards; }
@keyframes slideIn { from { transform: translateX(-100%);} to { transform: translateX(0);} }
@keyframes fadeIn { from { opacity:0;} to { opacity:1;} }
</style>