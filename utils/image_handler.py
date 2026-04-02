"""
Módulo para manejo de imágenes con PILLOW
"""
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil


class ImageHandler:

    def __init__(self):
        self.formatos_permitidos = ['.jpg', '.jpeg', '.png', '.gif']
        self.tamano_maximo = 5 * 1024 * 1024  # 5MB
        self.carpeta_imagenes = "assets/images"

        # Crear carpeta si no existe
        if not os.path.exists(self.carpeta_imagenes):
            os.makedirs(self.carpeta_imagenes)

    def seleccionar_imagen(self):
        """Abrir diálogo para seleccionar imagen"""
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )

        if filename:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in self.formatos_permitidos:
                messagebox.showerror("Error", f"Formato no permitido. Use: {', '.join(self.formatos_permitidos)}")
                return None

            tamaño = os.path.getsize(filename)
            if tamaño > self.tamano_maximo:
                messagebox.showerror("Error", f"La imagen es muy grande. Máximo: 5MB")
                return None

            return filename
        return None

    def procesar_imagen(self, origen_path, nombre_archivo=None, tamaño=(200, 200)):
        """Procesar y guardar imagen"""
        try:
            img = Image.open(origen_path)

            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = bg

            # Redimensionar manteniendo aspecto
            img.thumbnail(tamaño, Image.Resampling.LANCZOS)

            # Crear nueva imagen con fondo blanco del tamaño exacto
            nueva_img = Image.new('RGB', tamaño, (255, 255, 255))
            x = (tamaño[0] - img.size[0]) // 2
            y = (tamaño[1] - img.size[1]) // 2
            nueva_img.paste(img, (x, y))

            # Generar nombre de archivo
            if not nombre_archivo:
                nombre_archivo = f"img_{hash(origen_path) % 1000000}.jpg"
            else:
                nombre_archivo = f"{nombre_archivo}.jpg"

            # Guardar imagen
            destino_path = os.path.join(self.carpeta_imagenes, nombre_archivo)
            nueva_img.save(destino_path, 'JPEG', quality=85)

            return destino_path

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar imagen:\n{str(e)}")
            return None

    def cargar_imagen_para_tk(self, imagen_path, tamaño=(150, 150)):
        """Cargar imagen para usar en Tkinter"""
        try:
            if not imagen_path or not os.path.exists(imagen_path):
                return None

            img = Image.open(imagen_path)
            img.thumbnail(tamaño, Image.Resampling.LANCZOS)

            return ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None