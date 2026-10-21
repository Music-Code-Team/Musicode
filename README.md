# Como leer el README
* Lo que está en negritas son comandos de copiar y pegar
* lo que está entre *{}* requiere modificación (por ejemplo una ruta personalizada o datos personales)

# Como importar el proyecto
1. git clone **https://github.com/Music-Code-Team/Musicode.git**
2. No lo se, pero por si acaso **git init**
3. Ver branchs locales y remotas **git branch -a**
4. En caso de no aparecer, actualizar git con **git fetch --all**
5. Para usar una branch **git checkout {nombreBranch}**

# Reglas de colaboración
1. Crear un virtual enviroment: **python -m venv venv**
2. Activar venv: **.\venv\Scripts\activate** en Windows
3. instalar dependencias: **pip install -r requirements.txt**
* **Al añadir librerías al proyecto, añadir su nombre comercial (pip {librería}) al archivo requierements.txt**

# Crear ejecutbale
1. Ejecutar **auto-py-to-exe** ó **python -m auto_py_to_exe** en terminal
2. Abrir la opción **Settings**
3. En la sección **Configuration** presionar **Import Config From JSON**
4. Si se está creando el ejecutable de la CLI usar la ruta **MusicCode/src/CLI/packaging-config-file.json**
4. Si se está creando el ejecutable de la GUI usar la ruta **MusicCode/src/GUI/packaging-config-file.json**
5. Presionar el boton grande **Convert .PY to .EXE**
6. El archivo ejecutable aparece en **MusicCode/output**



# Ejecutar CLI
## Python
* En terminal escribir **py Orquest.py tu/ruta/de/archivo**
## Ejecutable
* En terminal escribir **Orquest.py tu/ruta/de/archivo**

# Ejecutar GUI
## Python
* En terminal escribir **py Orquest.py tu/ruta/de/archivo**
## Ejecutable
* En terminal escribir **Orquest.py tu/ruta/de/archivo**