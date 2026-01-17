# Generador de Patrones de Punto de Cruz 🧵

Una herramienta sencilla en Python que convierte tus imágenes favoritas en patrones de punto de cruz listos para imprimir. Genera un archivo PDF completo con el esquema visual y la leyenda de colores DMC necesarios.

## Características ✨

*   **Conversión inteligente**: Transforma cualquier imagen (JPG, PNG) a un patrón pixelado.
*   **Colores DMC Reales**: Utiliza una paleta de colores basada en los hilos estándar DMC.
*   **PDF Listo para imprimir**:
    *   **Página 1**: El patrón visual con una cuadrícula clara para facilitar el conteo (celda a celda y guías de 10x10).
    *   **Página 2**: Leyenda detallada con códigos de color DMC, nombres, muestras de color y cantidad de puntos necesarios.
*   **Personalizable**: Ajusta el ancho del patrón en puntos (la altura se calcula automáticamente).

## Instalación 🛠️

1.  Clona este repositorio:
    ```bash
    git clone https://github.com/JvK84/generador-punto-de-cruz.git
    cd generador-punto-de-cruz
    ```

2.  Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso 🚀

Ejecuta el script `cross_stitch.py` desde la terminal pasando la imagen que quieres convertir:

```bash
python cross_stitch.py tu_imagen.jpg --width 100 --output mi_patron.pdf
```

### Argumentos:
*   `TU_IMAGEN`: (Obligatorio) Ruta al archivo de imagen de entrada.
*   `--width`: (Opcional) Ancho del patrón en número de puntos/cruz. Por defecto es **80**.
*   `--output`: (Opcional) Nombre del archivo PDF de salida. Por defecto es **patron.pdf**.

### Ejemplo:

```bash
python cross_stitch.py luna.jpg --width 120 --output patron_luna.pdf
```

## Estructura del Proyecto TB

*   `cross_stitch.py`: Script principal de la aplicación.
*   `dmc_colors.py`: Base de datos con la información de los colores DMC.
*   `requirements.txt`: Lista de librerías de Python requeridas.

## Licencia 📄

Este proyecto es de uso libre. ¡Disfruta creando tus bordados!
