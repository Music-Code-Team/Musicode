//? ejemplo cómo llamar a python al hacer clic ene le botón de Play
async function handleRunCode() {
    let codigoEditor = document.getElementById("editor").ariaValueMax;
    //? O le valor del editor

    let response = await window.pywebview.api.run_code(codigoEditor);

    if (response.status === "succes") {
        console.log(response.message, "success");
    } else {
        console.error(response.message, "error");
        mostrarEnConsola(response.message,"error")
    }
}