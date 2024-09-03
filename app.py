import os
from os.path import join, dirname
from dotenv import load_dotenv
import uuid
from pymongo import MongoClient
import jwt #pip install pyjwt 
from datetime import datetime, timedelta 
import hashlib #untuk enkripsi, sudah bawaan
from flask import (
    Flask, 
    render_template, 
    jsonify, 
    request,
    redirect, 
    url_for )
from werkzeug.utils import secure_filename
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
SECRET_KEY = os.environ.get("SECRET_KEY")
TOKEN_KEY = os.environ.get("TOKEN_KEY")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET']) #UNTUK HALAMAN INDEX
def home():
    return render_template('index.html')

@app.route('/halaman_mahasiswa', methods=['GET']) #UNTUK HALAMAN INDEX
def halaman_mahasiswa():
    thelist = (
        db.prodi.find({}, {"_id": False}))

    output = []

    for i in thelist:
        output.append(i)

    listmahasiswa = (
        db.mahasiswa.find({}, {"_id": False}))

    outputmahasiswa = []

    for i in listmahasiswa:
        outputmahasiswa.append(i)

    return render_template('mahasiswa.html', output= output ,mahasiswa=outputmahasiswa)
    
@app.route('/tambah_mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    nama_receive = request.form['nama_mahasiswa']
    nim_receive =  request.form['nim']
    alamat_receive = request.form['alamat']
    kd_prodi_receive = request.form['kd_prodi']
    theId = f"{uuid.uuid1()}"
    doc = {
            "uuid": theId,
            "nama": nama_receive,
            "nim": nim_receive,
            "alamat": alamat_receive,
            "kode_prodi" : kd_prodi_receive
        }
    db.mahasiswa.insert_one(doc)
    return redirect(url_for('halaman_mahasiswa'))

@app.route("/edit-mahasiswa/<uuid>", methods=["POST"])
def edit_mahasiswa(uuid):
    nama_receive = request.form['editnama_mahasiswa']
    nim_receive =  request.form['editnim']
    alamat_receive = request.form['editalamat']
    kd_prodi_receive = request.form['editkd_prodi']
    new_doc = {
        "uuid": uuid,
        "nama": nama_receive,
        "nim": nim_receive,
        "alamat": alamat_receive,
        "kode_prodi" : kd_prodi_receive
    }

    db.mahasiswa.update_one({"uuid": uuid}, {"$set": new_doc})
    return redirect(url_for('halaman_mahasiswa'))

@app.route('/hapus_mahasiswa', methods=['POST'])  
def delete_mahasiswa():
    id_receive = request.form.get('id_give')  
    db.mahasiswa.delete_one({'uuid' : id_receive})
    return jsonify({ 'result' : 'success' , 'msg' : f'Data mahasiswa berhasil dihapus'})
# BE mahasiswa End

@app.route('/halaman_dosen', methods=['GET']) #UNTUK HALAMAN INDEX
def halaman_dosen():
    listoutputdosen = (
        db.dosen.find({}, {"_id": False}))

    outputdosen = []

    for i in listoutputdosen:
        outputdosen.append(i)

    return render_template('dosen.html', dosen=outputdosen)

@app.route('/tambah_dosen', methods=['POST'])
def tambah_dosen():
    kddosen_receive =  request.form['kd_dosen']
    nama_receive = request.form['nama_dosen']
    alamat_receive = request.form['alamat']
    theId = f"{uuid.uuid1()}"
    doc = {
            "uuid": theId,
            "kode_dosen": kddosen_receive,
            "nama_dosen": nama_receive,
            "alamat" : alamat_receive
        }
    db.dosen.insert_one(doc)
    return redirect(url_for('halaman_dosen'))

@app.route("/edit-dosen/<uuid>", methods=["POST"])
def edit_dosen(uuid):
    kddosen_receive =  request.form['editkd_dosen']
    nama_receive = request.form['editnama_dosen']
    alamat_receive = request.form['alamat']
    new_doc = {
        "uuid": uuid,
        "kode_dosen": kddosen_receive,
        "nama_dosen": nama_receive,
        "alamat" : alamat_receive,
    }

    db.dosen.update_one({"uuid": uuid}, {"$set": new_doc})
    return redirect(url_for('halaman_dosen'))

@app.route('/hapus_dosen', methods=['POST'])  
def delete_dosen():
    id_receive = request.form.get('id_give')  
    db.dosen.delete_one({'uuid' : id_receive})
    return jsonify({ 'result' : 'success' , 'msg' : f'Data dosen berhasil dihapus'})

@app.route('/halaman_prodi', methods=['GET']) #UNTUK HALAMAN INDEX
def halaman_prodi():
    thelist = (
        db.dosen.find({}, {"_id": False}))

    output = []

    for i in thelist:
        output.append(i)

    listoutputprodi = (
        db.prodi.find({}, {"_id": False}))

    outputprodi = []

    for i in listoutputprodi:
        outputprodi.append(i)

    return render_template('prodi.html' ,dosen=output , prodi=outputprodi)

@app.route('/tambah_prodi', methods=['POST'])
def tambah_prodi():
    kdprodi_receive = request.form['kd_prodi']
    namaprodi_receive = request.form['prodi']
    kddosen_receive = request.form['kd_dosen']
    theId = f"{uuid.uuid1()}"
    doc = {
            "uuid": theId,
            "kode_prodi": kdprodi_receive,
            "nama_prodi": namaprodi_receive,
            "kode_dosen": kddosen_receive
        }
    db.prodi.insert_one(doc)
    return redirect(url_for('halaman_prodi'))

@app.route("/edit-prodi/<uuid>", methods=["POST"])
def edit_prodi(uuid):
    kdprodi_receive = request.form['editkd_prodi']
    namaprodi_receive = request.form['editprodi']
    kddosen_receive = request.form['editkd_dosen']
    new_doc = {
        "uuid": uuid,
        "kode_prodi": kdprodi_receive,
        "nama_prodi": namaprodi_receive,
        "kode_dosen": kddosen_receive
    }
    db.prodi.update_one({"uuid": uuid}, {"$set": new_doc})
    return redirect(url_for('halaman_prodi'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=2000, debug=True)

