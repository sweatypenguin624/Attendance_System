# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from datetime import datetime
# from pdf_generator import txt_to_pdf


# def send_attendance_email(teacher_email, attendance_file):
#     # Gmail sender details
#     sender_email = "yogeshsoni230305@gmail.com"    # Replace with your Gmail address
#     password = "lvlz wzwi mrbb vqoe"         # Replace with your 16-character App Password
    
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     subject = f"Attendance Report - {current_date}"
#     body = f"""
#     Dear Teacher,
    
#     Please find attached the attendance report for {current_date}. 
#     The file contains student names and their attendance timestamps as recorded 
#     by the facial recognition system.
    
#     Regards,
#     Attendance System
#     {sender_email}
#     """
    
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = teacher_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         with open(attendance_file, "rb") as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header(
#                 'Content-Disposition',
#                 f'attachment; filename=attendance_{current_date}.txt'
#             )
#             msg.attach(part)
#     except FileNotFoundError:
#         print(f"Attendance file not found: {attendance_file}")
#         return
    
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()  # Enable TLS
#         server.login(sender_email, password)
#         server.send_message(msg)
#         server.quit()
#         print(f"Attendance email sent successfully to {teacher_email}")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

# if __name__ == "__main__":
#     teacher_email = "yogeshsoni233005@gmail.com"          # Replace with teacher's email
#     attendance_file = "G:/attendance_sys-main/attendance_2025-04-08.txt"
#     send_attendance_email(teacher_email, attendance_file)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# --- TXT to PDF Function ---
def txt_to_pdf(input_txt_path, output_pdf_path):
    try:
        if not os.path.exists(input_txt_path):
            return f"Error: Input file {input_txt_path} does not exist!"

        data_dict = {}
        with open(input_txt_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    filename = parts[0].strip()
                    name_parts = filename.split('_')
                    if len(name_parts) >= 2:
                        name = name_parts[0].capitalize()
                        usn_last_three = name_parts[1]
                        usn = f"1MV024RI{usn_last_three}"
                        time = parts[1].strip()
                        data_dict[usn_last_three] = [usn, name, time, "Present"]

        if not data_dict:
            return "Error: No valid data found in the text file!"

        data = []
        for i in range(1, 54):
            usn_num = f"{i:03d}"
            usn = f"1MV024RI{usn_num}"
            if usn_num in data_dict:
                data.append(data_dict[usn_num])
            else:
                data.append([usn, "", "", "Absent"])

        doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Student Attendance Report", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        table_data = [["USN", "Name", "Time", "Status"]]
        table_data.extend(data)

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

        table._argW[0] = 150
        table._argW[1] = 150
        table._argW[2] = 100
        table._argW[3] = 80

        elements.append(table)
        doc.build(elements)
        return f"PDF successfully created at {output_pdf_path}"

    except Exception as e:
        return f"Error creating PDF: {str(e)}"

# --- Email Sender ---
def send_attendance_email(teacher_email, attendance_txt_file):
    sender_email = "yogeshsoni230305@gmail.com"
    password = "lvlz wzwi mrbb vqoe"
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Attendance Report - {current_date}"
    body = f"""
    Dear Teacher,

    Please find attached the attendance report for {current_date}.
    The file contains student names and their attendance timestamps as recorded 
    by the facial recognition system.

    Regards,
    Attendance System
    {sender_email}
    """

    # Convert txt to PDF
    pdf_file = attendance_txt_file.replace(".txt", ".pdf")
    result = txt_to_pdf(attendance_txt_file, pdf_file)
    if "Error" in result:
        print(result)
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = teacher_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(pdf_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename=attendance_{current_date}.pdf'
            )
            msg.attach(part)
    except FileNotFoundError:
        print(f"Attendance file not found: {pdf_file}")
        return
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print(f"Attendance email sent successfully to {teacher_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- MAIN ---
if __name__ == "__main__":
    teacher_email = "adkm818@gmail.com"
    attendance_file = "G:/attendance_sys-main/attendance_2025-04-08.txt"
    send_attendance_email(teacher_email, attendance_file)
