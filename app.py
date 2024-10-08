from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd

# Import your functions here
from pyt import leChef1, natures_online, natures, santaMonica, usf, wcPrime, ifs, iD, mbc, rb

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            option = request.form.get('option')
            
            # Call the appropriate function based on user input
            if option == '1':
                result = leChef1(file_path)
            elif option == '2':
                result = natures_online(file_path)
            elif option == '3':
                result = natures(file_path)
            elif option == '4':
                result = santaMonica(file_path)
            elif option == '5':
                result = usf(file_path)
            elif option == '6':
                result = wcPrime(file_path)
            elif option == '7':
                result = ifs(file_path)
            elif option == '8':
                result = iD(file_path)
            elif option == '9':
                result = mbc(file_path)
            elif option == '10':
                result = rb(file_path)
            else:
                result = "Invalid selection"

            # Save the result to an Excel file
            excel_filename = f"{filename.rsplit('.', 1)[0]}_result.xlsx"
            excel_path = os.path.join(app.config['DOWNLOAD_FOLDER'], excel_filename)
            df = pd.DataFrame(result, columns=["Invoice No", "Net Amount", "Invoice Date"])
            df.to_excel(excel_path, index=False)

            # Display the result and the download link
            return render_template('index.html', result=result, download_link=url_for('download_file', filename=excel_filename))
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5008, debug=True)
