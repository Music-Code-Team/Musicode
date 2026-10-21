# Archivo principal de la GUI

import pywebview as webview
import pipreqs
import auto_py_to_exe

window = webview.create_window('Woah dude!', 'assets/index.html')
webview.start()