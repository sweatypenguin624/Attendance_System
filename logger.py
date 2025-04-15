from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def txt_to_pdf(input_txt_path, output_pdf_path):
    """
    Convert a text file with Name,Time,Distance to a formatted PDF with USN, Name, Time, Status.
    Includes all USNs from 001 to 053, sorted, with Absent marked for missing USNs.
    
    Args:
        input_txt_path (str): Path to input text.
        output_pdf_path (str): Path to save the output PDF.
    
    Returns:
        str: Success or error message.
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_txt_path):
            return f"Error: Input file {input_txt_path} does not exist!"

        # Read the text file
        data_dict = {}
        with open(input_txt_path, 'r') as file:
            lines = file.readlines()
            # Skip header
            for line in lines[1:]:
                # Split and clean the line
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    # Extract name and USN from filename (e.g., abhay_002_1.jpeg)
                    filename = parts[0].strip()
                    name_parts = filename.split('_')
                    if len(name_parts) >= 2:
                        name = name_parts[0].capitalize()
                        usn_last_three = name_parts[1]
                        # Construct USN (assuming format 1MV024RIXXX)
                        usn = f"1MV024RI{usn_last_three}"
                        time = parts[1].strip()
                        data_dict[usn_last_three] = [usn, name, time, "Present"]

        if not data_dict:
            return "Error: No valid data found in the text file!"

        # Create data for all USNs from 001 to 053
        data = []
        for i in range(1, 54):  # 001 to 053
            usn_num = f"{i:03d}"  # Format as 001, 002, etc.
            usn = f"1MV024RI{usn_num}"
            if usn_num in data_dict:
                data.append(data_dict[usn_num])
            else:
                data.append([usn, "", "", "Absent"])

        # Create PDF
        doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
        elements = []

        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph("Student Attendance Report", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))  # Add some space

        # Create table data
        table_data = [["USN", "Name", "Time", "Status"]]  # Header
        table_data.extend(data)

        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Adjust column widths
        table._argW[0] = 150  # USN
        table._argW[1] = 150  # Name
        table._argW[2] = 100  # Time
        table._argW[3] = 80   # Status

        elements.append(table)

        # Build PDF
        doc.build(elements)
        return f"PDF successfully created at {output_pdf_path}"

    except Exception as e:
        return f"Error creating PDF: {str(e)}"

# Example usage
if _name_ == "_main_":
    input_file = "input.txt"
    output_file = "output.pdf"
    result = txt_to_pdf(input_file, output_file)
    print(result)