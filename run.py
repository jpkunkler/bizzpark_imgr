import os
from os.path import basename
from flask import Flask, request, redirect, url_for, flash, send_file, render_template
from werkzeug.utils import secure_filename
import io
import shutil
from zipfile import ZipFile

from convert import addIcon

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum file size 16MB

# SETUP FOLDERS
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)
os.makedirs(os.path.join("converted"), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/download")
def download_files():
    memory_file = io.BytesIO()
    with ZipFile(memory_file, 'w') as zf:
        files = os.listdir(os.path.join(app.root_path, "converted"))
        for individualFile in files:
            folderpath = os.path.join(app.root_path, "converted", individualFile)
            for f in os.listdir(folderpath):
                filepath = os.path.join(folderpath, f)
                zf.write(filepath, basename(filepath)) # only add last part of our path to zip --> image file!    
    memory_file.seek(0)

    # clean up & recreate directories
    shutil.rmtree(os.path.join("converted"))
    shutil.rmtree(app.config["UPLOAD_FOLDER"])
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)
    os.makedirs(os.path.join("converted"), exist_ok=True)

    return send_file(memory_file, attachment_filename='{}.zip'.format(basename(folderpath)), as_attachment=True)

@app.route("/upload", methods=["GET", "POST"])
def handle_upload():
    if request.method == 'POST':
            # check if the post request has the file part
            if not request.files.getlist("file[]"):
                flash('No file part')
                return redirect(request.url)

            files = request.files.getlist('file[]')
            building = request.form["building_id"]
            company = request.form["text_name"].replace(" ", "_").lower()
            
            for f in files:
                if f and allowed_file(f.filename):
                    print(f)
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # convert uploaded files now
            files = os.listdir(os.path.join(app.root_path, "uploads"))
            for individualFile in files:
                path = os.path.join(app.root_path, "uploads", individualFile)
                img, directory, outfile = addIcon(path, building, company, os.path.join(app.root_path, "converted"))
                img.save(os.path.join(directory,outfile), "JPEG")

            return redirect(url_for('download_files'))

@app.route("/")
def index():
    return render_template('index.html') 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)