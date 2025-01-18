from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

hostname = "gofmw.h.filess.io"
database = "myproject_dancetouch"
port = "3305"
username = "myproject_dancetouch"
password = "8ca0969a6b13a27a107f7ad0e2acf1bc1ff576a1"

def create_connection():
    """ Create a database connection """
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port
        )
        if connection.is_connected():
            print("Connected to MariaDB Server")
            return connection
    except Error as e:
        print("Error while connecting to MariaDB", e)
        return None

@app.route('/')
def halaman_awal():
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_konser")
        result = cursor.fetchall()
        cursor.close()
    except Error as e:
        print("Error fetching data:", e)
        return "Error fetching data from the database.", 500
    finally:
        connection.close()

    return render_template('home.html', hasil=result)

@app.route('/home')
def halaman_home():
    return render_template('index.html')

@app.route('/concert')
def halaman_concert():
    return render_template('concert.html')

@app.route('/contact')
def halaman_contact():
    return render_template('contact.html')

@app.route('/hindia')
def halaman_hindia():
    return render_template('hindia.html')

@app.route('/denny caknan')
def halaman_denny_caknan():
    return render_template('denny caknan.html')

@app.route('/bernadya')
def halaman_bernadya():
    return render_template('bernadya.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    try:
        # Tangkap data form
        nama_lengkap = request.form['nama_lengkap']
        email = request.form['email']
        nomer_handphone = request.form['nomer_handphone']
        jumlah_tiket = int(request.form['jumlah_tiket'])  # Konversi ke integer
        
        # Mengambil total_harga dan membersihkannya
        total_harga_str = request.form['total_harga']  # Ambil string dari form
        total_harga_str = total_harga_str.replace('Rp. ', '').replace('.', '').strip()  # Hapus 'Rp.' dan titik
        total_harga = float(total_harga_str)  # Konversi ke float
        
        # Format ulang total_harga untuk ditampilkan
        total_harga_formatted = f'Rp. {total_harga:,.2f}'  # Format dengan dua desimal dan simbol Rp.
        
        nama_konser = request.form['nama_konser']
        
        # Debug: Print data yang akan diinsert
        print("Data yang akan diinsert:")
        print(f"Nama: {nama_lengkap}, Email: {email}, No HP: {nomer_handphone}, Jumlah Tiket: {jumlah_tiket}, Total Harga: {total_harga_formatted}, Nama Konser: {nama_konser}")

        connection = create_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return "Error: Unable to connect to the database.", 500

        try:
            cursor = connection.cursor()
            query = '''INSERT INTO tbl_konser 
                       (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser) 
                       VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (nama_lengkap, email, nomer_handphone, jumlah_tiket, total_harga, nama_konser)
            
            # Print query and values to be inserted
            print(f"Executing query: {query}")
            print(f"Values to insert: {values}")  # Print values to be inserted
            
            cursor.execute(query, values)
            connection.commit()
            return redirect(url_for('pembayaran_sukses'))  # Redirect to the success page
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return f"Error inserting data: {err.msg}", 500
            
        finally:
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"General Error: {e}")
        return f"Error processing form data: {e}", 500
    
@app.route('/pembayaran_sukses')
def pembayaran_sukses():
    return render_template('pembayaran_sukses.html')

if __name__ == '__main__':
    app.run(debug=True)
