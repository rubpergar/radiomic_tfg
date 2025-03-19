# Radiomic TFG

Este repositorio contiene los scripts relativos al Trabajo de Fin de Grado (TFG) sobre radiómicas de Rubén Pérez Garrido.

## Instalación

Para utilizar estos scripts, es necesario instalar varias dependencias. A continuación, se detallan los pasos para preparar el entorno correctamente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/rubpergar/radiomic_tfg.git
cd radiomic_tfg
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Es aconsejable crear un entorno virtual para instalar las dependencias necesarias para el funcionamiento de los scripts:

```bash
python -m venv venv
```

Activamos el entorno virtual:

```bash
source venv/bin/activate  # En Windows usar: venv\Scripts\activate
```

### 3. Instalar dependencias

Se recomienda utilizar `pip` para instalar las dependencias necesarias:

```bash
pip install numpy
```

```bash
pip install pyradiomics pydicom
```

### 4. Instalar Plastimatch

Plastimatch es una herramienta externa necesaria para la conversión de imágenes médicas. Sigue estos pasos para instalarlo:

1. Descarga el instalador desde la página oficial:  
   🔗 [Plastimatch Downloads](https://plastimatch.org/download.html)
2. Ejecuta el instalador y sigue las instrucciones.
3. **Añade Plastimatch al PATH** (si el instalador no lo hace automáticamente):
   - Abre `Variables de entorno` en Windows.
   - En la variable `Path`, agrega la ruta donde se instaló `plastimatch.exe` (por ejemplo, `C:\Program Files\Plastimatch\bin`).
4. Verifica la instalación ejecutando en PowerShell o CMD:

```sh
plastimatch --version
```

Si ves la versión, significa que está instalado correctamente.

### 5. Verificar la instalación

Para comprobar que todo está instalado correctamente, puedes ejecutar el siguiente script:

```bash
python -c "import numpy, radiomics, pydicom; print('Instalación correcta')"
```

Si no se muestra ningún error, el entorno está correctamente configurado.

## Contenido del repositorio

- `scripts/`: Contiene los scripts en Python necesarios para el análisis.
- `README.md`: Este archivo de documentación.

## Contacto

Si tienes alguna duda o problema con la instalación, puedes abrir un issue en el repositorio o contactar conmigo.
