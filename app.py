from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'galaxy_celenganku_key'

db_path = 'finance.db'
log_path = 'logs.txt'
data_path = 'data.json'

def get_balance():
    if not os.path.exists(data_path):
        return 0
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data.get('saldo', 0)

def update_balance(new_balance):
    with open(data_path, 'w') as f:
        json.dump({'saldo': new_balance}, f)

def save_transaction(jenis, jumlah):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'a') as f:
        f.write(f"[{now}] {jenis}: {jumlah}\n")

@app.route('/')
def index():
    saldo = get_balance()
    return render_template('index.html', saldo=saldo)

@app.route('/transaksi', methods=['POST'])
def transaksi():
    jenis = request.form['jenis']
    jumlah = int(request.form['jumlah'])
    saldo = get_balance()

    if jenis == 'tambah':
        saldo += jumlah
        flash(f"Berhasil menambahkan Rp {jumlah}", "success")
    elif jenis == 'tarik':
        if jumlah > saldo:
            flash("Saldo tidak cukup!", "danger")
            return redirect(url_for('index'))
        saldo -= jumlah
        flash(f"Berhasil menarik Rp {jumlah}", "success")

    update_balance(saldo)
    save_transaction(jenis, jumlah)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
