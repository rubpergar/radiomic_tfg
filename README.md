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

### 0. Requisitos previos

Descarga e instala la versión de Python 3.10.9 desde [python.org](https://www.python.org/downloads/release/python-3109/).  
> Durante la instalación marque la casilla de agregar al PATH del sistema para que este sea reconocido.

Verifica que esté correctamente instalado ejecutando en terminal o CMD:

```bash
python --version
```

> Deberá devolver `Python 3.10.9`

Este proyecto ha sido desarrollado usando Python 3.10.9 ya que es la mejor versión por estabilidad y compatibilidad con las dependencias usadas en el proyecto.

Algunas dependencias como `pyradiomics` tiene partes escritas en C++, por lo que es necesario tener instaladas herramientas de compilación de C++ de Microsoft. Para ello, descarga e instala **Microsoft C++ Build Tools**. Sigue estos pasos para instalarlo:
1. Descargar desde la página oficial:  
   🔗 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/)
2. Ejecutar el instalador y seguir las instrucciones.
3. Una vez instalado selecciona la opción de `Desarrollo para el escritorio con C++` y le das al botónde Instalar de abajo a la derecha.
<div align="center"> 
  <a> 
    <img width="700px" src="https://github.com/user-attachments/assets/ee511225-5297-4dda-98dd-8f2da366a3bb" alt="Captura Microsoft C++ Build Tools" />
  </a>
</div>


### 1. Clonar el repositorio

Clonación en local del repositorio:

```bash
git clone https://github.com/rubpergar/tfg-radiomicas.git
cd tfg-radiomicas
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
2. Ejecuta el instalador y sigue las instrucciones:
   - **¡IMPORTANTE!** Cuando pregunte en las opciones de instalación si quieres añadir Plastimatch al PATH, selecciona que **si** (o para el usuario actual o para todos los del sistema).
<div align="center"> 
  <a> 
    <img width="400px" src="https://github.com/user-attachments/assets/a1c4d11d-2da9-40a1-b682-ac03f00dacee" alt="Captura instalación Plastimatch" />
  </a>
</div>


### 5. Verificar la instalación

Para comprobar que todo está instalado correctamente, cierra la consola si la tiene abierta y vuélvela a abrir. Tras esto puedes ejecutar el siguiente script:

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
