# Radiomic TFG

Este repositorio contiene los scripts necesarios para el Trabajo de Fin de Grado (TFG) sobre radiómicas.

## Instalación

Para utilizar estos scripts, es necesario instalar varias dependencias y aplicaciones externas. A continuación, se detallan los pasos para preparar el entorno correctamente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/rubpergar/radiomic_tfg.git
cd radiomic_tfg
```

### 2. Crear un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows usar: venv\Scripts\activate
```

### 3. Instalar dependencias

Se recomienda utilizar `pip` para instalar las dependencias necesarias. Puedes instalarlas directamente desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Instalar SimpleITK y otras dependencias adicionales (si es necesario)

Algunas bibliotecas pueden requerir instalación manual dependiendo del sistema operativo:

```bash
pip install SimpleITK numpy pydicom nrrd pyradiomics
```

### 5. Verificar la instalación

Para comprobar que todo está instalado correctamente, puedes ejecutar el siguiente script:

```bash
python -c "import SimpleITK, numpy, pydicom, nrrd, radiomics; print('Instalación correcta')"
```

Si no se muestra ningún error, el entorno está correctamente configurado.

## Contenido del repositorio

- `scripts/`: Contiene los scripts en Python necesarios para el análisis.
- `data/`: Directorio sugerido para almacenar datos DICOM y NRRD.
- `README.md`: Este archivo de documentación.
- `requirements.txt`: Lista de dependencias necesarias.

## Contacto

Si tienes alguna duda o problema con la instalación, puedes abrir un issue en el repositorio o contactar conmigo.
