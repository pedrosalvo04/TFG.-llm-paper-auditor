"""
Script para convertir archivos Markdown o TXT a PDF
Utiliza markdown2 y reportlab para generar PDFs profesionales
"""
import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

try:
    import markdown2
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("⚠️ Advertencia: markdown2 no instalado. Solo se soportará conversión básica.")
    print("   Instala con: pip install markdown2")

def parse_markdown_to_elements(md_text, styles):
    """
    Convierte texto Markdown a elementos de reportlab
    
    Args:
        md_text: Texto en formato Markdown
        styles: Estilos de reportlab
        
    Returns:
        Lista de elementos para el PDF
    """
    elements = []
    lines = md_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Línea vacía
        if not line:
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Título nivel 1 (# Título)
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            elements.append(Paragraph(text, styles['Heading1']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Título nivel 2 (## Título)
        elif line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            elements.append(Paragraph(text, styles['Heading2']))
            elements.append(Spacer(1, 0.15*inch))
        
        # Título nivel 3 (### Título)
        elif line.startswith('### '):
            text = line[4:].strip()
            elements.append(Paragraph(text, styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Lista con viñetas (- item o * item)
        elif line.startswith('- ') or line.startswith('* '):
            text = '• ' + line[2:].strip()
            elements.append(Paragraph(text, styles['Normal']))
        
        # Lista numerada (1. item)
        elif len(line) > 2 and line[0].isdigit() and line[1:3] in ['. ', ') ']:
            elements.append(Paragraph(line, styles['Normal']))
        
        # Bloque de código (```)
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            elements.append(Preformatted(code_text, styles['Code']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Separador horizontal (---)
        elif line.startswith('---') or line.startswith('==='):
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph('<hr/>', styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Texto normal
        else:
            # Procesar negritas y cursivas básicas
            text = line
            text = text.replace('**', '<b>').replace('**', '</b>')
            text = text.replace('*', '<i>').replace('*', '</i>')
            elements.append(Paragraph(text, styles['Normal']))
        
        i += 1
    
    return elements

def convert_to_pdf(input_path, output_path=None, page_size='letter'):
    """
    Convierte un archivo Markdown o TXT a PDF
    
    Args:
        input_path: Ruta al archivo MD o TXT
        output_path: Ruta de salida (opcional)
        page_size: Tamaño de página ('letter' o 'a4')
        
    Returns:
        Ruta al archivo PDF generado
    """
    # Verificar que el archivo existe
    if not os.path.exists(input_path):
        print(f"❌ Error: El archivo '{input_path}' no existe")
        return None
    
    # Verificar extensión
    ext = input_path.lower().split('.')[-1]
    if ext not in ['md', 'txt', 'markdown']:
        print(f"❌ Error: '{input_path}' no es un archivo MD o TXT")
        return None
    
    # Determinar ruta de salida
    if output_path is None:
        output_path = input_path.rsplit('.', 1)[0] + '.pdf'
    
    try:
        print(f"📄 Convirtiendo: {input_path}")
        print(f"⏳ Procesando...")
        
        # Leer el archivo
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Configurar tamaño de página
        pagesize = A4 if page_size.lower() == 'a4' else letter
        
        # Crear PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=pagesize,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para código
        styles.add(ParagraphStyle(
            name='Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            textColor=colors.HexColor('#2d2d2d'),
            backColor=colors.HexColor('#f5f5f5'),
            borderPadding=5
        ))
        
        # Ajustar estilos existentes
        styles['Normal'].fontSize = 11
        styles['Normal'].leading = 14
        styles['Normal'].alignment = TA_JUSTIFY
        
        styles['Heading1'].fontSize = 18
        styles['Heading1'].textColor = colors.HexColor('#1a1a1a')
        styles['Heading1'].spaceAfter = 12
        
        styles['Heading2'].fontSize = 14
        styles['Heading2'].textColor = colors.HexColor('#2d2d2d')
        styles['Heading2'].spaceAfter = 10
        
        styles['Heading3'].fontSize = 12
        styles['Heading3'].textColor = colors.HexColor('#404040')
        styles['Heading3'].spaceAfter = 8
        
        # Convertir contenido a elementos
        elements = parse_markdown_to_elements(content, styles)
        
        # Generar PDF
        doc.build(elements)
        
        # Estadísticas
        file_size = os.path.getsize(output_path)
        page_count = len(elements) // 30  # Estimación aproximada
        
        print(f"✅ Conversión exitosa!")
        print(f"📊 Estadísticas:")
        print(f"   - Archivo generado: {output_path}")
        print(f"   - Tamaño: {file_size:,} bytes")
        print(f"   - Páginas (aprox.): {page_count}")
        print(f"   - Formato: {page_size.upper()}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error durante la conversión: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def convert_folder(folder_path, output_folder=None, page_size='letter'):
    """
    Convierte todos los archivos MD/TXT de una carpeta a PDF
    
    Args:
        folder_path: Ruta a la carpeta con archivos
        output_folder: Carpeta de salida (opcional)
        page_size: Tamaño de página
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: La carpeta '{folder_path}' no existe")
        return
    
    # Buscar todos los archivos MD y TXT
    md_files = list(Path(folder_path).glob('*.md'))
    txt_files = list(Path(folder_path).glob('*.txt'))
    all_files = md_files + txt_files
    
    if not all_files:
        print(f"⚠️ No se encontraron archivos MD o TXT en '{folder_path}'")
        return
    
    print(f"📁 Encontrados {len(all_files)} archivos")
    print("=" * 60)
    
    # Crear carpeta de salida si se especificó
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    # Convertir cada archivo
    successful = 0
    failed = 0
    
    for i, file in enumerate(all_files, 1):
        print(f"\n[{i}/{len(all_files)}]")
        
        if output_folder:
            output_path = os.path.join(output_folder, file.stem + '.pdf')
        else:
            output_path = None
        
        result = convert_to_pdf(str(file), output_path, page_size)
        
        if result:
            successful += 1
        else:
            failed += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 Resumen:")
    print(f"   ✅ Exitosos: {successful}")
    print(f"   ❌ Fallidos: {failed}")
    print(f"   📁 Total: {len(all_files)}")

def main():
    """Función principal con interfaz de línea de comandos"""
    print("=" * 60)
    print("📄 Conversor de Markdown/TXT a PDF")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📖 Uso:")
        print("   python md_to_pdf.py <archivo.md>")
        print("   python md_to_pdf.py <archivo.txt>")
        print("   python md_to_pdf.py <archivo.md> <salida.pdf>")
        print("   python md_to_pdf.py <archivo.md> --size a4")
        print("   python md_to_pdf.py --folder <carpeta>")
        print("   python md_to_pdf.py --folder <carpeta> --output <carpeta_salida>")
        print("\n💡 Ejemplos:")
        print("   python md_to_pdf.py paper.md")
        print("   python md_to_pdf.py paper.txt output.pdf")
        print("   python md_to_pdf.py paper.md --size a4")
        print("   python md_to_pdf.py --folder ./markdown")
        print("   python md_to_pdf.py --folder ./markdown --output ./pdfs")
        print("\n📏 Tamaños de página:")
        print("   - letter (default): 8.5 x 11 pulgadas")
        print("   - a4: 210 x 297 mm")
        return
    
    # Determinar tamaño de página
    page_size = 'letter'
    if '--size' in sys.argv:
        size_idx = sys.argv.index('--size')
        if size_idx + 1 < len(sys.argv):
            page_size = sys.argv[size_idx + 1]
    
    # Modo carpeta
    if sys.argv[1] == '--folder':
        if len(sys.argv) < 3:
            print("❌ Error: Especifica la carpeta")
            return
        
        folder_path = sys.argv[2]
        output_folder = None
        
        if '--output' in sys.argv:
            output_idx = sys.argv.index('--output')
            if output_idx + 1 < len(sys.argv):
                output_folder = sys.argv[output_idx + 1]
        
        convert_folder(folder_path, output_folder, page_size)
    
    # Modo archivo único
    else:
        input_path = sys.argv[1]
        output_path = None
        
        # Buscar output path (no confundir con --size)
        if len(sys.argv) >= 3 and not sys.argv[2].startswith('--'):
            output_path = sys.argv[2]
        
        convert_to_pdf(input_path, output_path, page_size)

if __name__ == "__main__":
    main()
