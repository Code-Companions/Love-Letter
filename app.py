from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Render the form page
    return render_template('index.html')

@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    # Get data from form
    sender_name = request.form['sender_name']
    recipient_name = request.form['recipient_name']
    message = request.form['message']
    special_memory = request.form['special_memory']
    
    # Handle uploaded image
    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)  # Sanitize filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)  # Save image to the uploads folder
            image_url = url_for('static', filename=f'uploads/{filename}')  # Correct URL for static files

    # Pass data and image URL to the letter template
    return render_template(
        'letter.html',
        sender_name=sender_name,
        recipient_name=recipient_name,
        message=message,
        special_memory=special_memory,
        image_url=image_url
    )

if __name__ == '__main__':
    app.run(debug=True)
