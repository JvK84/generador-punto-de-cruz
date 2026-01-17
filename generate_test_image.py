
from PIL import Image, ImageDraw

def create_test_image():
    # Crear imagen de 200x200
    img = Image.new('RGB', (200, 200), color='white')
    d = ImageDraw.Draw(img)
    
    # Dibujar algunas formas con colores que se parezcan a los DMC definidos
    d.rectangle([50, 50, 150, 150], fill=(255, 0, 0)) # Rojoish
    d.ellipse([20, 20, 80, 80], fill=(0, 0, 255))   # Azulish
    d.polygon([(100, 10), (190, 100), (100, 190)], fill=(0, 255, 0)) # Verdeish
    
    img.save('j:/Javier/PuntoDeCruz/test_image.png')
    print("Test image created.")

if __name__ == "__main__":
    create_test_image()
