<a name="readme-top"></a>

<div align="center">

<a> 
  <img width="300px" src="https://www.us.es/sites/default/files/inline-images/US-marca-principal.png" alt="LogoUS" />
</a>

# TFG Radiómicas | Rubén Pérez Garrido

Repositorio de scripts correspondientes al Trabajo de Fin de Grado (TFG) sobre radiómicas de **Rubén Pérez Garrido**, desarrollado en la **Universidad de Sevilla**.

</div>

<details>
<summary>Tabla de contenidos</summary>

- [Guía de uso](#guía-de-uso)
- [Características principales](#características-principales)
- [Instalación](#instalación)
  - [1. Clonar el repositorio](#1-clonar-el-repositorio)
  - [2. Crear un entorno virtual](#2-crear-un-entorno-virtual-opcional-pero-recomendado)
  - [3. Instalar dependencias](#3-instalar-dependencias)
  - [4. Instalar Plastimatch](#4-instalar-plastimatch)
  - [5. Verificar la instalación](#5-verificar-la-instalación)
- [Contenido del repositorio](#contenido-del-repositorio)
- [Contacto](#contacto)

</details>

---

## Guía de uso

Para aprender a usar los scripts, se puede consultar la sección [Wiki](https://github.com/rubpergar/radiomic_tfg/wiki), donde se ofrece una guía paso a paso para convertir imágenes CT y SEG en un conjunto de características radiómicas estables para su análisis.

## Características principales
- **Conversión de DICOM a NRRD**: Conversión individual o grupal de imágenes en formato DICOM a NRRD para facilitar su estudio y extracción de radiómicas.
- **Extracción de radiómicas**: Obtener características radiómicas a partir de las imágenes CT y SEG para poder estudiar la región de interés (ROI).
- **Estudio estadístico de radiómicas**: Obtener aquellas características radiómicas más estables para casos de estudio de pacientes a lo largo del tiempo.

<div align="center"> 
  <a> 
    <img width="700px" src="https://github.com/user-attachments/assets/183e662a-ef60-4380-9f0d-9389f23dcfbe" alt="Captura menú aplicación" />
  </a>
</div>

## Instalación

A continuación, se describen los pasos necesarios para configurar el entorno de trabajo.

### 1. Clonar el repositorio

Clonación en local del repositorio:

```bash
git clone https://github.com/rubpergar/radiomic_tfg.git
cd radiomic_tfg
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Crear un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
```

Activamos el entorno virtual:

- **Windows**
  ```cmd
  venv\Scripts\activate
  ```

- **Linux / macOS**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias

Se recomienda utilizar `pip` para instalar las dependencias necesarias:

```bash
pip install numpy
```
> Es necesario instalar `numpy` primero, ya que algunas de las demás dependencias la requieren y podrían fallar si no está instalada previamente.


```bash
pip install pyradiomics pydicom pynrrd pandas scikit-learn pingouin questionary argparse colorama
```

### 4. Instalar Plastimatch

Plastimatch es una herramienta externa necesaria para la conversión de imágenes médicas. Sigue estos pasos para instalarlo:

1. Descargar desde la página oficial:  
   🔗 [Plastimatch Downloads](https://sourceforge.net/projects/plastimatch/)
2. Ejecutar el instalador y seguir las instrucciones.
3. Añadir `Plastimatch` al PATH del sistema:
   - Abrir las **Variables de entorno** en Windows.
   - Editar la variable `Path` y añadir la ruta donde se instaló `plastimatch.exe`, por ejemplo:  
     `C:\Program Files\Plastimatch\bin`

### 5. Verificar la instalación

Para comprobar que todo está instalado correctamente, puedes ejecutar el siguiente script:

```bash
python -c "import numpy, radiomics, pydicom, nrrd, pandas, sklearn, pingouin, questionary, argparse, colorama; print('Instalación correcta')"
```
> Si no se muestra ningún error, el entorno está correctamente configurado.

Y posteriormente para comprobar si Plastimatch está correctamente instalado ejecuta:

```bash
plastimatch --version
```
> Si aparece la versión, está listo para usarse.


## Contenido del repositorio

- `data/`: Datos para realizar el tutorial de ejemplo.
- `scripts/`: Scripts principales en Python.
- `utils/`: Funciones auxiliares para simplificar el código.
- `main.py`: Punto de entrada principal para la ejecución del proyecto.
- `README.md`: Documento actual con guía de uso e instalación.

## Contacto

Si tienes dudas o encuentras algún problema, puedes abrir un [issue](https://github.com/rubpergar/radiomic_tfg/issues) o contactar directamente conmigo en **rubpergar@alum.us.es**.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>
