import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

# Configurar logging
log_path = os.path.join(os.path.expanduser('~'), 'Documents', 'OrganizadorDescargas')
if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(
    filename=os.path.join(log_path, 'organizador_log.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def create_folders(download_path):
    # Definir las carpetas base y sus extensiones correspondientes
    folders = {
        'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'],
        'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx'],
        'Archivos': ['.json', '.csv', '.xml', '.sql', '.db'],
        'Instaladores': ['.exe', '.msi', '.dmg', '.pkg', '.deb'],
        'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac'],
        'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
        'Otros': []
    }
    
    # Crear las carpetas si no existen
    for folder in folders.keys():
        new_folder = os.path.join(download_path, folder)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            logging.info(f"Creada nueva carpeta: {folder}")
    
    return folders

def organize_downloads():
    # Usar la ruta específica de tu carpeta de descargas
    download_path = r"C:\Users\Aleja\Downloads"
    
    # Verificar si la carpeta existe
    if not os.path.exists(download_path):
        logging.error(f"Error: La carpeta {download_path} no existe")
        return
    
    logging.info("=== Iniciando organización de descargas ===")
    
    # Crear las carpetas base
    folders = create_folders(download_path)
    
    # Contador de archivos movidos
    files_moved = 0
    
    # Recorrer todos los archivos en la carpeta de descargas
    for filename in os.listdir(download_path):
        file_path = os.path.join(download_path, filename)
        
        # Ignorar si es una carpeta
        if os.path.isdir(file_path):
            continue
        
        # Obtener la extensión del archivo
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Encontrar la carpeta correspondiente para el archivo
        destination_folder = 'Otros'  # Por defecto
        
        for folder, extensions in folders.items():
            if file_extension in extensions:
                destination_folder = folder
                break
        
        # Construir la ruta de destino
        destination_path = os.path.join(download_path, destination_folder, filename)
        
        # Verificar si el archivo ya existe en el destino
        if os.path.exists(destination_path):
            base, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(destination_path):
                new_filename = f"{base}_{counter}{extension}"
                destination_path = os.path.join(download_path, destination_folder, new_filename)
                counter += 1
        
        # Mover el archivo
        try:
            shutil.move(file_path, destination_path)
            files_moved += 1
            logging.info(f"Movido: {filename} -> {destination_folder}")
        except Exception as e:
            logging.error(f"Error al mover {filename}: {str(e)}")

    logging.info(f"Resumen: Total de archivos movidos: {files_moved}")
    logging.info("=== Organización completada ===\n")

if __name__ == "__main__":
    organize_downloads()