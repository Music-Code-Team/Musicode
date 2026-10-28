# Archivo principal de la GUI
import os
import sys
import webview

#? añadir la carpeta ráiz del proyecto al sys.path para importar el motor y compiler/CLI
current_dir = os.path.dirname(os.path.abspath(__file__)) #? importar motor o parser cuando se requiera
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

#? importar el módulo de compilación o parser real
#* si el compilador está en src/Compiler o src/CLI
try:
    #!ajustar importación según el nombre del archivo de compilación o parser
    #* from src.Compiler.parser import parse_code
    pass
except ImportError:
    pass

class KodaIDEApi:
    """
    Clase expuesta a Javasritp para el control, lectura y ejecución de archivos
    """
    def __init__(self):
        self.current_file_path = None

    def run_code(self, code_text):
        """
        Ejecuta el código .koda enviado desde el editor web
        """
        
        try:
            if not code_text or not code_text.strip():
                return {"status": "error", "message": "El editor esta vació."}
            
            print("[BACKEND] Compilando y ejecutando código .koda...")

            #! llamar parser / motor real -------------
            #! parse_sring(code_text)

            return {
                "status": "succes",
                "message": "Compilación y reproducción exitosa desde el Motor"
            }
        except Exception as e:
            return{"status": "error", "message": f"Error de ejecución: {str(e)}"}


class Api:
    """
    Conexión entre JavaScript (Front) y Python (Back)
    Cualquier método escrito aquí puede ser llamado desde JS usando pywebview.api.metodo()
    """


    def load_file_dialog(self):
        """
        Ventana para seleccionar archivos .koda
        """
        window = webview.windows[0]
        file_types = ('Archivos koda (*.koda)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)

        if result:
            self.current_file_path = result[0]
            
            try:
                with open(self.current_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "status": "success", 
                    "path": self.current_file_path,
                    "filename": os.path.basename(self.current_file_path), 
                    "content": content}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "cancelled"}

    def save_file(self, code_text):
        """
        Guarda el códgio actual en el archivo abierto
        """

        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    f.write(code_text)
                return {"status": "success", "path": self.current_file_path}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            #? Si no hay archivo abierto, se toma como un "Guardar como"
            return self.save_file_as(code_text)

    def save_file_as(self, code_text):
        """
        Abre dialogo para Guardar como
        """
        window = webview.windows[0]
        result = window.create_file_dialog(webview.SAVE_DIALOG, save_filename='nuevo.koda')
        if result:
            try:
                with open(result, 'w', encoding='utf-8') as f:
                    f.write(code_text)
                return{"status": "success", "path": result}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "cancelled"}

if __name__ == '__main__':
    api = KodaIDEApi()

    #? ruta al index.html dentro de GUI
    htlm_path = os.path.join(current_dir, 'index.html')

    window = webview.create_window(
        title='MusiCode IDE - Koda Studio',
        url=f'file://{htlm_path}',
        js_api=api,
        width=1300,
        height=750,
        background_color='#1e1e1e'
    )

    webview.start (debug=True) #? permite abrir las herramientas de desarrollo


