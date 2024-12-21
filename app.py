from flask import Flask, render_template, request, url_for, send_file
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF

app = Flask(__name__)

# Folder to store uploaded images and PDFs
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    sender_name = request.form['sender_name']
    recipient_name = request.form['recipient_name']
    message = request.form['message']
    special_memory = request.form['special_memory']
    
    # Handle uploaded image
    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{filename}')

    # Generate PDF
    letter_path = create_pdf(sender_name, recipient_name, message, special_memory, image_url)

    return render_template(
        'letter.html',
        sender_name=sender_name,
        recipient_name=recipient_name,
        message=message,
        special_memory=special_memory,
        image_url=image_url,
        letter_path=letter_path
    )



def create_pdf(sender_name, recipient_name, message, special_memory, image_url):
    """Function to generate a PDF letter."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"A Letter for {recipient_name}", ln=True, align='C')

    # Content
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Dear {recipient_name},", ln=True)
    pdf.multi_cell(0, 10, txt=message)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"One of my favorite memories with you is: \"{special_memory}\".", ln=True)

    # Add Image if Available
    if image_url:
        image_path = os.path.join(os.getcwd(), 'static', 'uploads', image_url.split('/')[-1])
        try:
            pdf.ln(10)
            pdf.image(image_path, x=50, w=100)
        except RuntimeError:
            pass  # Ignore if image fails to load

    pdf.ln(10)
    pdf.cell(200, 10, txt="With all my love,", ln=True)
    pdf.cell(200, 10, txt=sender_name, ln=True)

    # Save PDF
    pdf_output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"letter_{recipient_name}.pdf")
    pdf.output(pdf_output_path)

    return pdf_output_path


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
