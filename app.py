# PRIMER PARCIAL - DESARROLLO DE APLICACIONES WEB
# Canavirir Chura Diana
# GRUPO A

# INVENTARIO DE SISTEMA DE GESTION DE INVENTARIO DE UNA TIENDA DE TECNOLOGIA CLOUD

from flask import Flask, request, render_template, redirect, url_for
import sqlite3


app = Flask(__name__)

# Base de datos SQLite

def init_database():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS productos 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()
    
#inicializar la creacion de la Base de Datos y Tablas
init_database()

@app.route('/')
def index():
    #Conectar a la base de datos
    conn = sqlite3.connect('inventario.db')
    #Permite acceder a los datos de la base de datos como diccionarios
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', productos=productos)

#insertar los productos a la base de datos,. se obtiene los datos del formulario y se inserta en la tabla productos
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
       
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)
            ''',
            (nombre, categoria, precio, stock)
        )
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

#editar los productos, se obtiene el id del producto a editar, se muestra el formulario para editar, se actualiza la tabla productos con los nuevos datos
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        
        cursor.execute(
            '''
            UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?
            ''',
            (nombre, categoria, precio, stock, id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('edit.html', producto=producto)

#eliminar los productos, se obtiene el id del producto a eliminar, se elimina de la tabla productos
@app.route('/eliminar/<int:id>')
def eliminar(id):
    
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        DELETE FROM productos WHERE id = ?
        ''',
        (id,)
    )
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)