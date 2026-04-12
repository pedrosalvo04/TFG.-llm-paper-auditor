"""
Script para convertir archivos PDF a Markdown
Utiliza pymupdf4llm para una conversión optimizada para LLMs
"""
import os
import sys
import pymupdf4llm
from pathlib import Path

def convert_pdf_to_md(pdf_path, output_path=None):
    """
    Convierte un archivo PDF a Markdown
    
    Args:
        pdf_path: Ruta al archivo PDF
        output_path: Ruta de salida (opcional). Si no se proporciona, 
                     se crea en la misma carpeta con extensión .md
    
    Returns:
        Ruta al archivo Markdown generado
    """
    # Verificar que el archivo existe
    if not os.path.exists(pdf_path):
        print(f"❌ Error: El archivo '{pdf_path}' no existe")
        return None
    
    # Verificar que es un PDF
    if not pdf_path.lower().endswith('.pdf'):
        print(f"❌ Error: '{pdf_path}' no es un archivo PDF")
        return None
    
    # Determinar ruta de salida
    if output_path is None:
        output_path = pdf_path.replace('.pdf', '.md')
    
    try:
        print(f"📄 Convirtiendo: {pdf_path}")
        print(f"⏳ Procesando...")
        
        # Convertir PDF a Markdown
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        # Guardar el resultado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_text)
        
        # Estadísticas
        file_size = os.path.getsize(output_path)
        char_count = len(md_text)
        line_count = md_text.count('\n')
        
        print(f"✅ Conversión exitosa!")
        print(f"📊 Estadísticas:")
        print(f"   - Archivo generado: {output_path}")
        print(f"   - Tamaño: {file_size:,} bytes")
        print(f"   - Caracteres: {char_count:,}")
        print(f"   - Líneas: {line_count:,}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error durante la conversión: {str(e)}")
        return None

def convert_folder(folder_path, output_folder=None):
    """
    Convierte todos los PDFs de una carpeta a Markdown
    
    Args:
        folder_path: Ruta a la carpeta con PDFs
        output_folder: Carpeta de salida (opcional)
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: La carpeta '{folder_path}' no existe")
        return
    
    # Buscar todos los PDFs
    pdf_files = list(Path(folder_path).glob('*.pdf'))
    
    if not pdf_files:
        print(f"⚠️ No se encontraron archivos PDF en '{folder_path}'")
        return
    
    print(f"📁 Encontrados {len(pdf_files)} archivos PDF")
    print("=" * 60)
    
    # Crear carpeta de salida si se especificó
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    # Convertir cada PDF
    successful = 0
    failed = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}]")
        
        if output_folder:
            output_path = os.path.join(output_folder, pdf_file.stem + '.md')
        else:
            output_path = None
        
        result = convert_pdf_to_md(str(pdf_file), output_path)
        
        if result:
            successful += 1
        else:
            failed += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 Resumen:")
    print(f"   ✅ Exitosos: {successful}")
    print(f"   ❌ Fallidos: {failed}")
    print(f"   📁 Total: {len(pdf_files)}")

def main():
    """Función principal con interfaz de línea de comandos"""
    print("=" * 60)
    print("🔄 Conversor de PDF a Markdown")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📖 Uso:")
        print("   python pdf_to_md.py <archivo.pdf>")
        print("   python pdf_to_md.py <archivo.pdf> <salida.md>")
        print("   python pdf_to_md.py --folder <carpeta>")
        print("   python pdf_to_md.py --folder <carpeta> --output <carpeta_salida>")
        print("\n💡 Ejemplos:")
        print("   python pdf_to_md.py paper.pdf")
        print("   python pdf_to_md.py paper.pdf output.md")
        print("   python pdf_to_md.py --folder ./papers")
        print("   python pdf_to_md.py --folder ./papers --output ./markdown")
        return
    
    # Modo carpeta
    if sys.argv[1] == '--folder':
        if len(sys.argv) < 3:
            print("❌ Error: Especifica la carpeta")
            return
        
        folder_path = sys.argv[2]
        output_folder = None
        
        if len(sys.argv) >= 5 and sys.argv[3] == '--output':
            output_folder = sys.argv[4]
        
        convert_folder(folder_path, output_folder)
    
    # Modo archivo único
    else:
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) >= 3 else None
        
        convert_pdf_to_md(pdf_path, output_path)

if __name__ == "__main__":
    main()
