"""Script para convertir el paper de prueba a PDF"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def create_test_paper_pdf():
    """Crea un PDF del paper de prueba con errores"""
    
    # Crear PDF en la misma carpeta que el script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_file = os.path.join(current_dir, "data", "paper_test_con_errores.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#000000'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Contenido
    story.append(Paragraph("Deep Learning for Image Classification: A Novel Approach", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Authors:</b> John Doe, Jane Smith", styles['Normal']))
    story.append(Paragraph("<b>Affiliation:</b> University of Example", styles['Normal']))
    story.append(Paragraph("<b>Year:</b> 2024", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Abstract
    story.append(Paragraph("<b>Abstract</b>", styles['Heading2']))
    story.append(Paragraph(
        "We propose a novel deep learning architecture for image classification that achieves "
        "state-of-the-art results. Our method outperforms previous approaches by a significant margin. "
        "Experiments show promising results on standard benchmarks.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 1. Introduction
    story.append(Paragraph("1. Introduction", styles['Heading2']))
    story.append(Paragraph(
        "Image classification is a fundamental task in computer vision. Recent advances in deep learning "
        "have shown impressive results. Our work builds upon these advances to create a better model.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 2. Related Work
    story.append(Paragraph("2. Related Work", styles['Heading2']))
    story.append(Paragraph(
        "Previous work in this area includes CNNs and ResNets. These models have been widely used. "
        "Our approach is different and better.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 3. Methodology
    story.append(Paragraph("3. Methodology", styles['Heading2']))
    story.append(Paragraph("3.1 Model Architecture", styles['Heading3']))
    story.append(Paragraph(
        "We use a neural network with multiple layers. The architecture consists of convolutional layers "
        "followed by fully connected layers. We apply dropout for regularization.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3.2 Training Procedure", styles['Heading3']))
    story.append(Paragraph(
        "We trained our model on a dataset. The training was performed using a GPU. "
        "We used an optimizer to minimize the loss function.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3.3 Hyperparameters", styles['Heading3']))
    story.append(Paragraph(
        "We tuned the hyperparameters to get good results.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 4. Experiments
    story.append(Paragraph("4. Experiments", styles['Heading2']))
    story.append(Paragraph("4.1 Dataset", styles['Heading3']))
    story.append(Paragraph(
        "We used a popular image dataset for our experiments.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.2 Results", styles['Heading3']))
    story.append(Paragraph(
        "Our model achieved good accuracy. The results are shown in the table below:",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Tabla de resultados
    data = [
        ['Model', 'Accuracy'],
        ['Ours', '95.2%'],
        ['Baseline', '92.1%']
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.3 Ablation Study", styles['Heading3']))
    story.append(Paragraph(
        "We performed ablation studies and found that all components are important.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 5. Implementation Details
    story.append(Paragraph("5. Implementation Details", styles['Heading2']))
    story.append(Paragraph(
        "The model was implemented in Python. We used some libraries.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 6. Computational Resources
    story.append(Paragraph("6. Computational Resources", styles['Heading2']))
    story.append(Paragraph(
        "Training took some time on our hardware.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 7. Data Availability
    story.append(Paragraph("7. Data Availability", styles['Heading2']))
    story.append(Paragraph(
        "The data is publicly available.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 8. Code Availability
    story.append(Paragraph("8. Code Availability", styles['Heading2']))
    story.append(Paragraph(
        "Code will be made available upon request.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # 9. Conclusion
    story.append(Paragraph("9. Conclusion", styles['Heading2']))
    story.append(Paragraph(
        "We presented a novel approach that works well. Future work will explore more applications.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # References
    story.append(Paragraph("References", styles['Heading2']))
    story.append(Paragraph("[1] Some paper about CNNs", styles['Normal']))
    story.append(Paragraph("[2] Another paper about deep learning", styles['Normal']))
    story.append(Paragraph("[3] A third relevant paper", styles['Normal']))
    
    # Generar PDF
    doc.build(story)
    print(f"✅ PDF creado: {pdf_file}")

if __name__ == "__main__":
    create_test_paper_pdf()
