import os
from os.path import basename
from flask import Flask, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import io
from zipfile import ZipFile

from convert import addIcon

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum file size 16MB

# create upload folder if it does not exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/download")
def download_files():
    memory_file = io.BytesIO()
    with ZipFile(memory_file, 'w') as zf:
        files = os.listdir(os.path.join(app.root_path, "uploads"))
        for individualFile in files:
            path = os.path.join(app.root_path, "uploads", individualFile)
            zf.write(path, basename(path)) # only add last part of our path to zip --> image file!
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='files.zip', as_attachment=True)

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if not request.files.getlist("file[]"):
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('file[]')
        for f in files:
            if f and allowed_file(f.filename):
                print(f)
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        files = os.listdir(os.path.join(app.root_path, "uploads"))
        for individualFile in files:
            path = os.path.join(app.root_path, "uploads", individualFile)
            building = request.form["building_id"]
            company = request.form["text_name"]
            img, directory, outfile = addIcon(path, building, company, os.path.join(app.root_path, "converted"))
            print(img, os.path.join(directory,outfile))
            img.save(os.path.join(directory,outfile), "JPEG")

    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>BIZZPARK App Image Converter</title>

</head>
<body>
    <div style="width:600px">
        
        <form action="" method="post" enctype="multipart/form-data">
        <ul>
        
            <li>
                <label for="select_id">Bitte Gebäudenummer auswählen</label>
                <select name="building_id" id="select_id">
                    <option value="01">01</option>
                    <option value="02">02</option>
                    <option value="value 3">03</option>
                    <option value="value 1">04</option>
                    <option value="value 1">05</option>
                    <option value="value 1">06</option>
                    <option value="value 1">07</option>
                    <option value="value 1">08</option>
                    <option value="value 1">09</option>
                    <option value="value 1">10</option>
                    <option value="value 1">11</option>
                    <option value="value 1">12</option>
                    <option value="value 1">13</option>
                    <option value="value 1">14</option>
                    <option value="value 1">15</option>
                    <option value="value 1">16</option>
                    <option value="value 1">17</option>
                    <option value="value 1">18</option>
                    <option value="value 1">19</option>
                    <option value="value 1">20</option>
                </select>
            </li>
        
            <li>
                <label for="text_id">Bitte Unternehmen auswählen</label>
                <input type="text" name="text_name" id="text_id" value=""/>
            </li>

            <li>
                <label>Wählen Sie die hochzuladenden Dateien von Ihrem Rechner aus:
                <input name="file[]" type="file" multiple> 
              </label> 
            </li>
            <li><button>hochladen</button></li>
            <li><a href="/download">Click me.</a></li>
        
        </ul>
        
        </form>
        
        </div>
</body>
</html>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)