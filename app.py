import os
import logging
import sqlite3
import threading
import time

from flask import Flask, render_template, request, make_response, g, redirect
from werkzeug.utils import secure_filename

data = {}
upload_folder = 'F:/myPrograms/Python/file_upload_api/upload_folder'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
log = logging.getLogger('pydrop')


@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello_world():
    return render_template('uploader.html', data=data)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['upload_file']
    print(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    if os.path.exists(save_path):
        return make_response(('File already exists', 400))
    try:
        with open(save_path, 'ab') as f:
            file_chunks = read_in_chunks(file)
            f.write(file_chunks.__next__())
        print("File Uploaded")
        params = (file.filename, "ACTIVE", 0)
        g.db.execute("INSERT INTO processingUploads (name,status,line_processed) values (?,?,?)", params)
        threading.Thread(target=start_processing_the_uploaded_file, args=(file.filename,)).start()
        g.db.commit()
        data[file.filename] = {'name': file.filename, 'active': "ACTIVE"}
        return redirect('/')
    except OSError:
        log.exception('Could not write to file')
        return redirect('/')
    except StopIteration:
        return redirect('/')


@app.route('/upload/pause/<name>', methods=['GET'])
def pause_upload(name):
    g.db.execute("UPDATE processingUploads set status='PAUSED' where name=?", (name,))
    data[name]['active'] = "PAUSED"
    g.db.commit()
    return redirect('/')


@app.route('/upload/resume/<name>', methods=['GET', ])
def resume_upload(name):
    g.db.execute("UPDATE processingUploads set status='ACTIVE' where name=?", (name,))
    g.db.commit()
    data[name]['active'] = 'ACTIVE'
    start_from = g.db.execute("SELECT line_processed from processingUploads where name=?", (name,))
    x = start_from.fetchone()[0]
    threading.Thread(target=start_processing_the_uploaded_file, args=(name, x + 1)).start()
    return redirect('/')


@app.route('/upload/cancel/<name>', methods=['GET', 'POST'])
def cancel_upload(name):
    g.db.execute("UPDATE processingUploads set status='CANCELLED' where name=?", (name,))
    data[name]['active'] = "CANCELLED"
    g.db.commit()
    return redirect('/')


def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.stream.read(chunk_size)
        if not data:
            break
        yield data


if __name__ == '__main__':
    app.run(threaded=True)


def start_processing_the_uploaded_file(file_name, start=0):
    conn = sqlite3.connect("database.db")
    sql_query = "SELECT status FROM processingUploads where name=?"
    update_query = "UPDATE processingUploads set line_processed = ? where name=?"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name))
    with open(file_path) as f:
        lines = f.readlines()
        for i in range(start, len(lines)):
            print("Reading Line " + str(i) + " : " + lines[i])
            time.sleep(1)
            res = conn.execute(sql_query, (file_name,))
            r = res.fetchone()[0]
            conn.execute(update_query, (i, file_name))
            conn.commit()
            if r == "PAUSED" or r == "CANCELLED":
                break
            if i == len(lines) - 1:
                conn.execute("UPDATE processingUploads set status='COMPLETE' where name=?", (file_name,))
                conn.commit()
                data[file_name]['active'] = "COMPLETE"
    conn.close()

