# Archivo principal de la GUI

import pywebview as webview
import pipreqs

window = webview.create_window('Woah dude!', 'assets/index.html')
webview.start()