import os
from os.path import join, dirname
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# client = MongoClient('mongodb+srv://test:sparta@cluster0.zo4xdve.mongodb.net/?retryWrites=true&w=majority')
# db = client.Cluster0
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, { '_id': False }))
    return jsonify({ 'diaries': diaries })

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files['file']
    prof_image = request.files['profImage']
    title = request.form['title']
    content = request.form['content']

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    # image
    extension = file.filename.split('.')[-1]
    image_file = f'file-{mytime}.{extension}'
    save_to = f'static/images/{image_file}'
    file.save(save_to)

    # profile image
    extension = prof_image.filename.split('.')[-1]
    prof_image_file = f'profile-{mytime}.{extension}'
    save_to = f'static/images/{prof_image_file}'
    prof_image.save(save_to)


    if title == '':
        return jsonify({ 'msg': 'Fill the title!' })
    elif content == '':
        return jsonify({ 'msg': 'Fill the content!' })
    else:
        doc = {
            'file': image_file,
            'profImage': prof_image_file,
            'title': title,
            'content': content
        }
        db.diary.insert_one(doc)
        return jsonify({ 'msg': 'Upload complete!' })
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)