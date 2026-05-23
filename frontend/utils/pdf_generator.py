# -*- coding: utf-8 -*-
"""
Generador de informes PDF de auditoría NeurIPS 2026.
Utiliza ReportLab para compilar un documento PDF profesional con veredictos,
tablas de cumplimiento coloreadas y bases de datos técnicas extraídas.
"""
import io
import datetime
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para realizar una doble pasada sobre el PDF.
    Esto permite calcular dinámicamente el número total de páginas y
    dibujar cabeceras y pies de página profesionales en cada hoja.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        w, h = self._pagesize
        
        # Color primario / secundario
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))
        
        margin_left = 54
        margin_right = w - 54
        
        # Cabecera (Header)
        self.drawString(margin_left, h - 40, "INFORME DE AUDITORÍA CIENTÍFICA")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(margin_right, h - 40, "Checklist NeurIPS 2026")
        
        # Línea divisoria cabecera
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(margin_left, h - 46, margin_right, h - 46)
        
        # Pie de página (Footer)
        self.line(margin_left, 55, margin_right, 55)
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(margin_right, 42, page_text)
        self.drawString(margin_left, 42, "Generado por Auditor Inteligente LLM")
        
        self.restoreState()


def md_to_reportlab_html(text):
    """
    Convierte sintaxis Markdown básica a etiquetas HTML compatibles con ReportLab.
    """
    if not text or text == "—":
        return "—"
    
    # Escapar caracteres HTML reservados que romperían el parseador de ReportLab
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Restaurar etiquetas básicas necesarias para formato
    # Reemplazar **negrita** por <b>negrita</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Reemplazar *cursiva* por <i>cursiva</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Reemplazar `código` por un tipo Courier
    text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
    
    return text


def generate_pdf_report(resultado, uploaded_file, health=None):
    """
    Genera un informe PDF profesional con ReportLab.
    
    Args:
        resultado: Dict con los resultados del análisis RAG/auditoría
        uploaded_file: Objeto de archivo cargado o nombre del archivo (string)
        health: Checklist health precalculado (opcional)
        
    Returns:
        Bytes del archivo PDF generado.
    """
    if health is None:
        from frontend.utils.scoring import get_checklist_health
        health = get_checklist_health(resultado)

    paper_name = uploaded_file if isinstance(uploaded_file, str) else uploaded_file.name
    
    # Buffer en memoria
    buffer = io.BytesIO()
    
    # Dimensiones de la página A4
    # A4 = 595.27 x 841.89 puntos
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    w_page, h_page = A4
    content_width = w_page - 108  # 487.27 puntos de ancho libre
    
    # --- Configurar Estilos ---
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        name='ReportSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        name='ReportH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        name='ReportH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        name='ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    center_text_style = ParagraphStyle(
        name='CenterText',
        parent=body_style,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        name='HeaderStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white
    )
    
    header_center_style = ParagraphStyle(
        name='HeaderCenterStyle',
        parent=header_style,
        alignment=TA_CENTER
    )
    
    badge_yes = ParagraphStyle(
        name='BadgeYesStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#065f46'),
        alignment=TA_CENTER
    )
    
    badge_no = ParagraphStyle(
        name='BadgeNoStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#b91c1c'),
        alignment=TA_CENTER
    )
    
    badge_na = ParagraphStyle(
        name='BadgeNaStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER
    )

    # --- 1. Título y Subtítulo ---
    story.append(Paragraph("Informe de Auditoría Científica", title_style))
    story.append(Paragraph("Evaluación automática de cumplimiento bajo los criterios oficiales NeurIPS 2026", subtitle_style))
    
    # --- 2. Tabla de Metadatos ---
    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    metricas = resultado.get("metricas", {})
    tiempo = metricas.get("tiempo_segundos", "N/A")
    caracteres = metricas.get("caracteres_leidos", "N/A")
    
    metadata_data = [
        [
            Paragraph("<b>Artículo:</b>", body_style),
            Paragraph(paper_name, body_style),
            Paragraph("<b>Fecha Auditoría:</b>", body_style),
            Paragraph(fecha_hoy, body_style)
        ],
        [
            Paragraph("<b>Tiempo Ejecución:</b>", body_style),
            Paragraph(f"{tiempo}s" if isinstance(tiempo, (int, float)) else str(tiempo), body_style),
            Paragraph("<b>Caract. Analizados:</b>", body_style),
            Paragraph(f"{caracteres:,}" if isinstance(caracteres, int) else str(caracteres), body_style)
        ]
    ]
    
    # Dividir el ancho de la página en columnas proporcionales
    col_w_meta = [75, 168.6, 100, 143.6]
    metadata_table = Table(metadata_data, colWidths=col_w_meta)
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 12))
    
    # --- 3. Banner de Veredicto ---
    status_label = "CHECKLIST VÁLIDO" if health["status"] == "valid" else "ATENCIÓN REQUERIDA"
    status_color = "#064e3b" if health["status"] == "valid" else "#b45309"
    status_bg = "#ecfdf5" if health["status"] == "valid" else "#fffbeb"
    status_border = "#10b981" if health["status"] == "valid" else "#f59e0b"
    status_text_color = "#047857" if health["status"] == "valid" else "#b45309"
    
    desc_text = (
        "Todas las respuestas del checklist tienen evidencia referenciada o una justificación adecuada para los revisores."
        if health["status"] == "valid"
        else f"Se han detectado {health['pending_count']} ítems que requieren atención o justificación obligatoria antes de proceder con el envío."
    )
    
    verdict_html = f"""
    <b><font size="11" color="{status_text_color}">&#x25C6; {status_label}</font></b><br/>
    <font size="9" color="#1e293b">{desc_text}</font>
    """
    verdict_p = Paragraph(verdict_html, body_style)
    
    verdict_table = Table([[verdict_p]], colWidths=[content_width])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(status_bg)),
        ('LINELEFT', (0, 0), (0, -1), 4, colors.HexColor(status_border)),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 12))
    
    # --- 4. Panel de Métricas ---
    yes_count = sum(1 for i in health["items"] if "yes" in i["answer"].lower())
    no_count = sum(1 for i in health["items"] if "no" in i["answer"].lower())
    na_count = sum(1 for i in health["items"] if "n/a" in i["answer"].lower())
    pending_count = health["pending_count"]
    
    metrics_data = [
        [
            Paragraph(f'<font size="13" color="#047857"><b>{yes_count}</b></font><br/><font size="7" color="#64748b">CUMPLE (YES)</font>', center_text_style),
            Paragraph(f'<font size="13" color="#b91c1c"><b>{no_count}</b></font><br/><font size="7" color="#64748b">NO CUMPLE (NO)</font>', center_text_style),
            Paragraph(f'<font size="13" color="#1e3a8a"><b>{na_count}</b></font><br/><font size="7" color="#64748b">NO APLICA (N/A)</font>', center_text_style),
            Paragraph(f'<font size="13" color="{status_color}"><b>{pending_count}</b></font><br/><font size="7" color="#64748b">PENDIENTES</font>', center_text_style)
        ]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[content_width/4.0]*4)
    metrics_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 16))
    
    # --- 5. Tabla de Cumplimiento ---
    story.append(Paragraph("Tabla de Cumplimiento NeurIPS 2026", h1_style))
    
    table_headers = [
        Paragraph("#", header_center_style),
        Paragraph("Item del Checklist", header_style),
        Paragraph("Respuesta", header_center_style),
        Paragraph("Evidencia / Justificación", header_style)
    ]
    
    table_rows = [table_headers]
    t_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')), # Encabezado negro
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    
    # Estilo de párrafo para celdas de texto
    cell_style = ParagraphStyle(
        name='CellText',
        parent=body_style,
        fontSize=8,
        leading=10.5,
        spaceAfter=0
    )
    
    num_style = ParagraphStyle(
        name='NumText',
        parent=cell_style,
        alignment=TA_CENTER
    )
    
    for idx, item in enumerate(health["items"], start=1):
        label = item["label"]
        if ". " in label:
            num, name = label.split(". ", 1)
        else:
            num, name = str(idx), label
            
        answer = item["answer"]
        evidence = item["evidence"]
        
        # Determinar badge de respuesta
        a_lower = answer.lower()
        if "yes" in a_lower:
            badge_p = Paragraph("YES", badge_yes)
        elif "no" in a_lower:
            badge_p = Paragraph("NO", badge_no)
        else:
            badge_p = Paragraph("N/A", badge_na)
            
        # Limpiar texto de evidencia y añadir alertas
        ev_clean = md_to_reportlab_html(evidence)
        ev_text = f"{ev_clean}"
        
        if item["pending_justification"]:
            ev_text += '<br/><font size="7" color="#b91c1c"><b>⚠️ Falta justificación explícita en el paper</b></font>'
        elif item["missing_evidence"]:
            ev_text += '<br/><font size="7" color="#b45309"><b>⚠️ Respuesta "Yes" sin evidencia directa</b></font>'
            
        if "compensacion" in item.get("alert_msg", "").lower() or "etica" in item.get("alert_msg", "").lower():
            ev_text += '<br/><font size="7" color="#b45309"><b>⚠️ Código de Ética: compensación mínima de crowdsourcing</b></font>'
            
        row_index = len(table_rows)
        table_rows.append([
            Paragraph(num, num_style),
            Paragraph(name, cell_style),
            badge_p,
            Paragraph(ev_text, cell_style)
        ])
        
        # Fondo suave según el cumplimiento del ítem
        if item["pending_justification"]:
            bg_color = "#fef2f2" # Rojo suave
        elif item["missing_evidence"]:
            bg_color = "#fffbeb" # Ámbar suave
        elif "yes" in a_lower:
            bg_color = "#f0fdf4" # Verde suave
        else:
            bg_color = "#f8fafc" # Gris/Azul suave
            
        t_styles.append(('BACKGROUND', (0, row_index), (-1, row_index), colors.HexColor(bg_color)))
        
    # Ancho total de columnas ajustado al content_width (487.27)
    checklist_table = Table(table_rows, colWidths=[20, 145, 52, 270.27])
    checklist_table.setStyle(TableStyle(t_styles))
    story.append(checklist_table)
    story.append(Spacer(1, 16))
    
    # --- 6. Ficha Técnica Consolidada (Reduce Database) ---
    info = resultado.get("informacion_extraida", {})
    
    section_config = {
        "hyperparameters": "Hiperparámetros & Configuración",
        "hardware": "Hardware & Computación",
        "architecture": "Arquitectura del Modelo",
        "data": "Dataset & Datos",
        "code": "Código & Repositorio",
        "statistics": "Estadística & Rigor Científico",
        "baseline_comparison": "Comparativa con Baselines",
        "theory_and_proofs": "Teoría & Demostraciones",
        "software_versions": "Software & Versiones",
        "limitations_quality": "Análisis de Limitaciones",
        "licenses_extraction": "Licencias de Código/Datos",
        "broader_impacts_extraction": "Impacto Social (Broader Impacts)",
        "llm_usage_extraction": "Declaración de uso de LLMs",
        "human_subjects_extraction": "Sujetos Humanos & Ética"
    }
    
    tech_story = []
    has_tech_data = False
    
    for key, label in section_config.items():
        data = info.get(key)
        if data and data != "NOT FOUND":
            if not has_tech_data:
                tech_story.append(Paragraph("Ficha Técnica y Datos Consolidados", h1_style))
                tech_story.append(Spacer(1, 4))
                has_tech_data = True
            
            tech_story.append(Paragraph(label, h2_style))
            
            if isinstance(data, dict):
                for k, v in data.items():
                    if v and v != "NOT FOUND":
                        k_clean = k.replace('_', ' ').title()
                        v_clean = md_to_reportlab_html(str(v))
                        p_text = f"• <b>{k_clean}:</b> {v_clean}"
                        tech_story.append(Paragraph(p_text, bullet_style))
            elif isinstance(data, list):
                for item in data:
                    item_clean = md_to_reportlab_html(str(item))
                    tech_story.append(Paragraph(f"• {item_clean}", bullet_style))
            else:
                data_clean = md_to_reportlab_html(str(data))
                tech_story.append(Paragraph(data_clean, body_style))
                
            tech_story.append(Spacer(1, 4))
            
    if tech_story:
        # Usamos KeepTogether para evitar saltos huérfanos de cabecera si es posible,
        # pero como el contenido puede ser grande, dejamos que fluya libremente en el story principal.
        story.extend(tech_story)
        
    # --- 7. Razonamiento (CoT) ---
    cot = info.get("thought_process")
    if cot and cot != "No disponible":
        story.append(Spacer(1, 10))
        story.append(Paragraph("Razonamiento del Auditor (Chain of Thought)", h1_style))
        cot_clean = md_to_reportlab_html(cot).replace("\n", "<br/>")
        story.append(Paragraph(cot_clean, body_style))
        
    # --- Compilar el documento ---
    doc.build(story, canvasmaker=NumberedCanvas)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
