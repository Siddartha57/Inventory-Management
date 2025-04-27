from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Reports
from flask import flash, redirect,request,Response, url_for
from module import db


def download_report():
    # Fetch data from the Reports table
    reports = Reports.query.all()

    if not reports:
        flash("No reports available to generate PDF.", "warning")
        return redirect(request.referrer)

    # Create a PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Stock Report")

    # Add title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Stock Report")

    # Set column headers
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 700, "Item Name")
    pdf.drawString(200, 700, "Quantity")
    pdf.drawString(300, 700, "Price")
    pdf.drawString(400, 700, "Time")

    y = 680  

    # Add report data to PDF
    pdf.setFont("Helvetica", 12)
    for report in reports:
        pdf.drawString(50, y, report.name)
        pdf.drawString(200, y, str(report.quantity))
        pdf.drawString(300, y, f"₹{report.price}")
        pdf.drawString(400, y, str(report.time))
        y -= 20  # Move to next line

    pdf.save()
    buffer.seek(0)

    # Clear the reports table after generating the PDF
    try:
        db.session.query(Reports).delete()
        db.session.commit()
        flash("PDF downloaded sucessfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing reports: {str(e)}", "danger")

    return Response(
        buffer,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Stock_Report.pdf"}
    )