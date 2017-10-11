import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and "file[]" in request.files:
        for f in request.files.getlist("file[]"):
            print(f.filename, allowed_file(f.filename))
            print(request.form["building_id"])
            print(request.form["text_name"])
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
        
        </ul>
        
        </form>
        
        </div>
</body>
</html>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)