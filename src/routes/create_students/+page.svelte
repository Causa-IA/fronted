<script>
    import { onMount } from "svelte";
    import HamburgerMenu from "$lib/HamburgerMenu.svelte";

    let facultades = [];
    let usuarios = [];
    let programas = [];

    let id_estudiante;
    let id_facultad; 
    let id_programa;
    let id_usuario;
    let primer_nombre;
    let primer_apellido;
    let tipo_identificacion;
    let numero_identificacion;
    let genero;
    let telefono;
    let direccion;
    let fecha_registro; 

    onMount(async () => {
        const response = await fetch("https://fastapi1-3jjn.onrender.com/usuarios/get_usuarios/")
        const data = await response.json();
        usuarios = data.resultado;
    })

    onMount(async () => {
        const response = await fetch("https://fastapi1-3jjn.onrender.com/facultades/get_facultades/");
        const data = await response.json();
        facultades = data.resultado;
    });

    $: if(id_facultad){
        fetchProgramas(id_facultad);
    } else {
        programas = [];
    }

    async function fetchProgramas(facultadId) {
        try {
            const response = await fetch(`https://fastapi1-3jjn.onrender.com/programas/get_programas_por_facultad/${facultadId}`);
            const data = await response.json();
            programas = data.resultado;
        } catch (error) {
            console.error("Error al cargar programas:", error);
        }
    }

    function limpiarCampos(data){
        Object.keys(data).forEach(key => {
            if(data[key] === "" || data[key] === undefined){
                data[key] = null;
            }
        });
        return data;
    }

    async function submitForm(event) {
        event.preventDefault();

        let formData = {
            id_estudiante,
            id_facultad,
            id_programa,
            id_usuario,
            primer_nombre,
            primer_apellido,
            tipo_identificacion,
            numero_identificacion,
            genero,
            telefono,
            direccion,
            fecha_registro
        }

        formData = limpiarCampos(formData);

        try {
            const response = await fetch("https://fastapi1-3jjn.onrender.com/estudiantes/create_estudiante", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            })

            const data = await response.json()

            if(response.ok){
                showNotification("✅ Estudiante registrado correctamente", "success");
                setTimeout(() => window.location.href = "/search_student", 1000);
            }else{
                showNotification(data.detail || "❌ Error al registrar estudiante", "error");
            }

        } catch (error) {
            console.error(error);
            showNotification("⚠️ Error de conexión", "error");
        }
    }

    function showNotification(message, type){
        const notif = document.getElementById("notification");
        notif.textContent = message;
        notif.className = "notification show " + type;
        setTimeout(()=> notif.classList.remove("show"), 1000);
    }
</script>

<HamburgerMenu />
<div id="notification" class="notification"></div>
<div class="container">
    <h1>Registro de estudiante</h1>
    <form on:submit={submitForm}>
    <div>
    <label>Facultad:
    <select bind:value={id_facultad} required>
    <option value="">Seleccione una facultad</option>
    {#each facultades as facultad}
    <option value={facultad.id_facultad}>{facultad.nombre}</option>
    {/each}
    </select>
    </label>
    </div>

    <div>
    <label>Programa
    <select bind:value={id_programa} required>
    <option value="">Seleccione un programa</option>
    {#each programas as programa}
    <option value={programa.id_programa}>{programa.nombre}</option>
    {/each}
    </select>
    </label>
    </div>

    <div>
    <label>Enfermera que registra el estudiante
    <select bind:value={id_usuario} required>
    <option value="">Seleccione usuario</option>
    {#each usuarios as usuario}
    <option value={usuario.id_usuario}>{usuario.primer_nombre + " " + usuario.primer_apellido}</option>
    {/each}
    </select>
    </label>
    </div>

    <div>
    <label>Primer Nombre
    <input type="text" bind:value={primer_nombre} placeholder="Primer nombre" required>
    </label>
    </div>

    <div>
    <label>Primer Apellido
    <input type="text" bind:value={primer_apellido} placeholder="Primer apellido" required>
    </label>
    </div>

    <div>
    <label>Tipo de Identificación
    <select bind:value={tipo_identificacion} required>
    <option value="">Seleccione</option>
    <option value="CC">Cédula</option>
    <option value="TI">Tarjeta de identidad</option>
    <option value="CE">Cédula de extranjería</option>
    </select>
    </label>
    </div>

    <div>
    <label>Número de Identificación
    <input type="text" bind:value={numero_identificacion} placeholder="Número de identificación" required>
    </label>
    </div>

    <div>
    <p class="genero">Género
    <label>Masculino
    <input type="radio" value="Masculino" bind:group={genero}>
    </label>

    <label>Femenino
    <input type="radio" value="Femenino" bind:group={genero}>
    </label>
    </p>
    </div>

    <div>
    <label>Teléfono
    <input type="tel" bind:value={telefono} placeholder="Número de teléfono">
    </label>
    </div>

    <div>
    <label>Dirección
    <input type="text" bind:value={direccion} placeholder="Dirección">
    </label>
    </div>

    <div>
    <label>Fecha de registro
    <input type="datetime-local" bind:value={fecha_registro} placeholder="Fecha de registro">
    </label>
    </div>

    <button type="submit">Agregar información</button>

    </form>
</div>

<style>

*{
  box-sizing: border-box;
}
:global(body){
  background: linear-gradient(135deg, #eff2f5, rgb(222, 227, 240));
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  font-family:"Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.container {
  max-width: clamp(320px, 90%, 750px);
  width: 100%;
  padding: 25px;   /* más espacio interno */
  border-radius: 20px;
  background: rgba(255,255,255,0.25);
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  backdrop-filter: blur(12px);            
  border: 1px solid rgba(255,255,255,0.18);
}

form{
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
    margin-top: 20px;
}

form div{
    margin-bottom: 18px;
}

label{
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 6px;
}

input, select{
    width: 100%;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid #dcdfe6;
    font-size: 14px;
    transition: all 0.2s ease;
}

input:focus, select:focus{
    outline: none;
    border-color: #2f80ed;
    box-shadow: 0 0 0 2px rgba(47,128,237,0.15);
}

input[type="radio"]{
    width: auto;
    margin-left: 6px;
    margin-right: 4px;
}

p{
    font-size: 14px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 8px;
}

h1{
  text-align:center;
  margin:0;   
  color:#1a237e;
  font-weight:700;
}

button {
  display: block;
  margin: 15px auto;
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s ease;
  width: auto;
}

button:hover{
  background:#1565c0;
  transform:scale(1.02);
}

button:active{
  transform:scale(0.98);
}

@media (min-width: 600px){

    form{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    form div{
        margin-bottom: 0;
    }

    button{
        grid-column: span 2;
        justify-self: center;
        width: 100%;
    }

}

:global(.notification){
  position:fixed;
  top:30px;
  left:50%;
  transform:translateX(-50%) translateY(-20px);
  padding:16px 24px;
  border-radius:10px;
  font-size:16px;
  font-weight:700;
  color:white;
  opacity:0;
  transition:opacity 0.4s ease, transform 0.4s ease;
  z-index:9999;
  max-width:90%;
  text-align:center;
}

:global(.notification.show){
    opacity:1;
    transform:translateX(-50%) translateY(0);
}

:global(.notification.success){
    background:#43a047;
    box-shadow:0 6px 20px rgba(67,160,71,0.4);
}

:global(.notification.error){
    background:#d32f2f;
    box-shadow:0 6px 20px rgba(211,47,47,0.4);
}

</style>

