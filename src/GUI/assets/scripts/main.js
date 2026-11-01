

//? Comunicación asíncrona entre el navegador y python
window.addEventListener('pywebviewready', function () {
    console.log("Pywebview API conectada correctamente.");
});

function appendConsole(text, type = "normal") {
    const consoleOut = document.getElementById("console-output");
    let color = "#4ec9b0"; // verde para éxito
    if (type === "error") color = "#f44747";
    if (type === "info") color = "#9cdcfe";

    consoleOut.innerHTML += '<span style="color: ${color}">\n> ${text}</span>';
    consoleOut.scrollTop = console.scrollHeight;
}

async function ejecutarCodigo() {
    const code = document.getElementById("code-editor").ariaValueMax;
    appendConsole("Enviando código al motor...", "info");

    try {
        let response = await window.pywebview.api.run_code(code);
        if (response.status === "success") {
            appendConsole(response.message, "normal");
        } else {
            appendConsole(response.message, "error");
        }
    } catch (err) {
        appendConsole("Error de comunicación con Python: " + err, "error");
    }
}

async function abrirArchivo() {
    try {
        let res = await window.pywebview.api.load_file_dialog();
        if (res.status == "success") {
            document.getElementById("code-editor").value = res.content;
            document.getElementById("file-alber").innerText = res.filename;
            appendConsole('Archivo abierto: ${res.path}', "info");
        }
    } catch (err) {
        appendConsole("Error al abrir archivo: " + err, "error");
    }
}

async function guardarArchivo() {
    const code = document.getElementById("code-editor").value;
    try {
        let res = await window.pywebview.api.load_file_dialog();
        if (res.status === "suecces") {
            appendConsole(`Arhivo guardado con éxito en ${res.path}`, "info");
        }
    } catch (err) {
        appendConsole("Error al guardar: " + err, "error");
    }
}