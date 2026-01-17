
import argparse
import sys
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import dmc_colors
import math

# Configuración
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm
DRAW_AREA_WIDTH = PAGE_WIDTH - 2 * MARGIN
DRAW_AREA_HEIGHT = PAGE_HEIGHT - 2 * MARGIN

def get_dmc_color(rgb_tuple):
    """Encuentra el color DMC más cercano."""
    min_dist = float('inf')
    best_color = None
    
    r1, g1, b1 = rgb_tuple
    
    for dmc in dmc_colors.DMC_COLORS:
        r2, g2, b2 = dmc['rgb']
        # Distancia Euclidiana simple (se puede mejorar con redmean o CIELAB)
        dist = math.sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)
        if dist < min_dist:
            min_dist = dist
            best_color = dmc
            
    return best_color

def process_image(image_path, width_stitches):
    """Procesa la imagen y genera la matriz de colores DMC."""
    img = Image.open(image_path)
    w, h = img.size
    aspect_ratio = h / w
    height_stitches = int(width_stitches * aspect_ratio)
    
    # Redimensionar
    img_small = img.resize((width_stitches, height_stitches), Image.Resampling.LANCZOS)
    img_rgb = img_small.convert('RGB')
    
    grid = []
    used_colors = {} # Para la leyenda: {code: count}
    
    pixels = img_rgb.load()
    
    for y in range(height_stitches):
        row = []
        for x in range(width_stitches):
            r, g, b = pixels[x, y]
            dmc = get_dmc_color((r, g, b))
            row.append(dmc)
            
            code = dmc['code']
            if code not in used_colors:
                used_colors[code] = {'info': dmc, 'count': 0}
            used_colors[code]['count'] += 1
            
        grid.append(row)
        
    return grid, used_colors, width_stitches, height_stitches

from reportlab.lib.pagesizes import A4, landscape, portrait

def create_pdf(output_filename, grid, used_colors, width, height, original_filename):
    # Determinar orientación óptima
    if width > height:
        page_size = landscape(A4)
        PAGE_WIDTH, PAGE_HEIGHT = page_size
    else:
        page_size = portrait(A4)
        PAGE_WIDTH, PAGE_HEIGHT = page_size

    c = canvas.Canvas(output_filename, pagesize=page_size)
    c.setTitle(f"Patrón de Punto de Cruz - {original_filename}")
    
    # Configuración de márgenes reducidos para ocupar más hoja
    MARGIN = 10 * mm
    TITLE_HEIGHT = 15 * mm # Espacio reservado para título
    
    DRAW_AREA_WIDTH = PAGE_WIDTH - 2 * MARGIN
    DRAW_AREA_HEIGHT = PAGE_HEIGHT - 2 * MARGIN - TITLE_HEIGHT
    
    # --- PÁGINA 1: DIBUJO DEL PATRÓN ---
    # Calcular tamaño de celda
    cell_w = DRAW_AREA_WIDTH / width
    cell_h = DRAW_AREA_HEIGHT / height
    cell_size = min(cell_w, cell_h)
    
    # Centrar el grid en el área de dibujo
    grid_width = cell_size * width
    grid_height = cell_size * height
    
    start_x = (PAGE_WIDTH - grid_width) / 2
    # El grid empieza justo debajo del título
    start_y_grid = PAGE_HEIGHT - MARGIN - TITLE_HEIGHT
    
    # Título más compacto
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 5*mm, f"Patrón: {original_filename} ({width}x{height})")
    
    # Dibujar grid
    c.setLineWidth(0.1)  # Línea fina para la grilla
    c.setStrokeColorRGB(0.5, 0.5, 0.5) # Gris medio
    
    for y in range(height):
        for x in range(width):
            dmc = grid[y][x]
            r, g, b = dmc['rgb']
            c.setFillColorRGB(r/255.0, g/255.0, b/255.0)
            
            rect_y = start_y_grid - (y + 1) * cell_size
            rect_x = start_x + x * cell_size
            
            c.rect(rect_x, rect_y, cell_size, cell_size, fill=1, stroke=1)
            
    # Líneas de cuadrícula 10x10 más gruesas
    c.setLineWidth(1.0)
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    
    # Líneas verticales
    for x in range(0, width + 1, 10):
        if x == 0 or x == width: continue 
        line_x = start_x + x * cell_size
        bottom_y = start_y_grid - height * cell_size
        c.line(line_x, start_y_grid, line_x, bottom_y)
        
    # Líneas horizontales
    for y in range(0, height + 1, 10):
        if y == 0 or y == height: continue
        line_y = start_y_grid - y * cell_size
        right_x = start_x + width * cell_size
        c.line(start_x, line_y, right_x, line_y)
            
    c.showPage()
    
    # --- PÁGINA 2: ESQUEMA DE COLORES (LEYENDA) ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, "Esquema de Colores (Leyenda)")
    
    entry_height = 10 * mm
    y_pos = PAGE_HEIGHT - MARGIN - 15 * mm
    
    # Ordenar por código
    sorted_codes = sorted(used_colors.keys(), key=lambda x: (len(x), x))
    
    c.setFont("Helvetica", 10)
    
    # Headers
    c.drawString(MARGIN, y_pos, "Muestra")
    c.drawString(MARGIN + 20*mm, y_pos, "Código DMC")
    c.drawString(MARGIN + 50*mm, y_pos, "Nombre")
    c.drawString(MARGIN + 120*mm, y_pos, "Puntos")
    y_pos -= 5*mm
    
    for code in sorted_codes:
        if y_pos < MARGIN:
            c.showPage()
            y_pos = PAGE_HEIGHT - MARGIN
            
        info = used_colors[code]['info']
        count = used_colors[code]['count']
        r, g, b = info['rgb']
        
        # Muestra de color
        c.setFillColorRGB(r/255.0, g/255.0, b/255.0)
        c.rect(MARGIN, y_pos - 4*mm, 10*mm, 4*mm, fill=1, stroke=1)
        
        # Texto
        c.setFillColorRGB(0, 0, 0)
        c.drawString(MARGIN + 20*mm, y_pos - 4*mm, str(code))
        c.drawString(MARGIN + 50*mm, y_pos - 4*mm, info['name'])
        c.drawString(MARGIN + 120*mm, y_pos - 4*mm, str(count))
        
        y_pos -= entry_height

    c.save()

def main():
    parser = argparse.ArgumentParser(description="Convierte una imagen a patrón de punto de cruz.")
    parser.add_argument("image", help="Ruta de la imagen de entrada")
    parser.add_argument("--width", type=int, default=80, help="Ancho del patrón en puntos (default: 80)")
    parser.add_argument("--output", default="patron.pdf", help="Nombre del archivo de salida (default: patron.pdf)")
    
    args = parser.parse_args()
    
    try:
        print(f"Procesando {args.image}...")
        grid, used_colors, w, h = process_image(args.image, args.width)
        print(f"Generado patrón de {w}x{h} puntos.")
        print(f"Colores únicos utilizados: {len(used_colors)}")
        
        create_pdf(args.output, grid, used_colors, w, h, args.image)
        print(f"PDF guardado en: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
