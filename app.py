import os
from config import app, db, jsonify, request, API_KEY, ALLOWED_EXTENSIONS
import models
from flask import render_template, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
from translate.languages import show_all_languages_translation
from translate.translate import Translator
import requests

# for uploaded files
UPLOAD_FOLDER = r'files/'

# for translated files
TRANSLATED = r'files/translated/'

# for uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# determine extension
def extensions(f_name):
    ext = f_name.split('.')[-1]
    return True if ext in ALLOWED_EXTENSIONS else False


# add language code to file name and set new path for translated files
def path_for_translated(path, lang):
    path = path.split('.')
    path.insert(-1, lang)
    path = '.'.join(path).split('/')
    path.insert(-1, 'translated')
    return '/'.join(path)


# download file using name from database
@app.route('/download/', methods=['POST'])
def download():
    if request.method == 'POST':
        f_id = request.form['f_id']
        schema = models.FileSchema()
        url = models.File.query.get(f_id)
        data = schema.dump(url)
        translated = data['translated_file']
        return send_from_directory('', translated, as_attachment=True)
    return redirect(url_for('upload'))


@app.route('/files', methods=['GET'])
def get_files():
    schema = models.FileSchema(many=True)
    files = models.File.query.order_by(models.File.id.desc())
    data = schema.dump(files)
    return jsonify(data)


# add file to database
def add_file(original, translated):
    success = False
    error = ''
    data = []
    try:
        new_file = models.File(original, translated)
        db.session.add(new_file)
        db.session.commit()
        db.session.refresh(new_file)
        data = {'id': new_file.id,
                'original_file': original,
                'translated': translated}

        success = True
    except Exception as e:
        error = str(e)
    finally:
        return {'success': success,
                'data': data,
                'error': error}


def translate_subtitles(file, lang):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # save original file

    # set new name and path for translated file
    out_file_name = path_for_translated(os.path.join(app.config['UPLOAD_FOLDER'] + filename), lang)

    tr = Translator(API_KEY, os.path.join(app.config['UPLOAD_FOLDER'], filename))
    translate = tr.translate_all(lang, out_file_name)  # translate function

    add_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), out_file_name)

    return translate


@app.route('/', methods=['GET', 'POST'])
def upload():
    BASE_URL = request.url_root
    data = {'languages': show_all_languages_translation(),
            'error': '',
            'translated': '',
            'db_content': [],
            }

    file_list = requests.get('{}files'.format(BASE_URL)).json()

    data['db_content'] = file_list

    if request.method == 'POST':
        file = request.files['file']
        lang = request.form['dest_lang']

        if (file.filename == '' and lang != '') or (file.filename != '' and lang == ''):
            data['error'] = 'Please choose file and language.'

        if file and extensions(file.filename):
            translate = translate_subtitles(file, lang)

            data['translated'] = translate

            # redirect to '/' route in order to reload database content
            return redirect(url_for('upload'))
    return render_template("upload.html", data=data)


if __name__ == '__main__':
    app.run()
