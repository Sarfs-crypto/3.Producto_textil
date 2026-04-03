
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from tkinter import filedialog, messagebox
import os
import hashlib

class ImageHandler:
    def __init__(self):
        self.formatos_permitidos = ['.jpg', '.jpeg', '.png', '.gif']
        self.tamano_maximo = 5 * 1024 * 1024  # 5MB
        self.carpeta_imagenes = "assets/images"
        self.tamano_thumbnail = (150, 150)
        self.tamano_guardado = (300, 300)

        # Crear carpeta si no existe
        os.makedirs(self.carpeta_imagenes, exist_ok=True)

    def seleccionar_imagen(self):
        """Abrir diálogo para seleccionar imagen con validación de formato y tamaño"""
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen para el producto",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )

        if filename:
            # Validar formato
            ext = os.path.splitext(filename)[1].lower()
            if ext not in self.formatos_permitidos:
                messagebox.showerror("Error",
                    f"Formato no permitido.\nFormatos soportados: {', '.join(self.formatos_permitidos)}")
                return None

            # Validar tamaño
            tamaño = os.path.getsize(filename)
            if tamaño > self.tamano_maximo:
                messagebox.showerror("Error",
                    f"La imagen es demasiado grande.\nTamaño máximo: {self.tamano_maximo // (1024*1024)}MB\n"
                    f"Tamaño actual: {tamaño // 1024}KB")
                return None

            return filename
        return None

    def procesar_imagen(self, origen_path, nombre_archivo=None, tamaño=None):
        """Procesar y guardar imagen (redimensionamiento, conversión, optimización)"""
        if tamaño is None:
            tamaño = self.tamano_guardado

        try:
            # Abrir imagen
            img = Image.open(origen_path)

            # Convertir a RGB si es necesario (eliminar canal alfa)
            if img.mode in ('RGBA', 'LA', 'P'):
                fondo = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                fondo.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
                img = fondo

            # Redimensionar manteniendo aspecto
            img.thumbnail(tamaño, Image.Resampling.LANCZOS)

            # Crear nueva imagen con fondo blanco del tamaño exacto
            nueva_img = Image.new('RGB', tamaño, (255, 255, 255))

            # Pegar imagen redimensionada centrada
            x = (tamaño[0] - img.size[0]) // 2
            y = (tamaño[1] - img.size[1]) // 2
            nueva_img.paste(img, (x, y))

            # Generar nombre de archivo único basado en hash
            if not nombre_archivo:
                hash_obj = hashlib.md5(origen_path.encode() + str(os.path.getmtime(origen_path)).encode())
                nombre_archivo = hash_obj.hexdigest()[:16]

            # Guardar imagen optimizada
            destino_path = os.path.join(self.carpeta_imagenes, f"{nombre_archivo}.jpg")
            nueva_img.save(destino_path, 'JPEG', quality=85, optimize=True)

            return destino_path

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen:\n{str(e)}")
            return None

    def cargar_thumbnail(self, imagen_path, tamaño=None):
        """Cargar imagen redimensionada para vista previa en Tkinter"""
        if tamaño is None:
            tamaño = self.tamano_thumbnail

        try:
            if not imagen_path or not os.path.exists(imagen_path):
                return None

            img = Image.open(imagen_path)
            img.thumbnail(tamaño, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"Error al cargar thumbnail: {e}")
            return None

    def aplicar_filtro(self, imagen_path, filtro):
        """Aplicar filtros a la imagen (para funcionalidad avanzada)"""
        try:
            img = Image.open(imagen_path)

            if filtro == "blur":
                img = img.filter(ImageFilter.BLUR)
            elif filtro == "contour":
                img = img.filter(ImageFilter.CONTOUR)
            elif filtro == "sharpen":
                img = img.filter(ImageFilter.SHARPEN)
            elif filtro == "emboss":
                img = img.filter(ImageFilter.EMBOSS)
            elif filtro == "brightness":
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.3)
            elif filtro == "contrast":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)

            # Guardar imagen con filtro
            nombre = f"filtrado_{os.path.basename(imagen_path)}"
            destino = os.path.join(self.carpeta_imagenes, nombre)
            img.save(destino, 'JPEG', quality=85)

            return destino

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro:\n{str(e)}")
            return None