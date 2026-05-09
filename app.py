from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# CONFIG MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbcrud'

mysql = MySQL(app)

# HTML WEB

@app.route('/')
def home():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    return render_template('index.html', users=users)


# AGREGAR DESDE FORMULARIO HTML
@app.route('/add', methods=['POST'])
def add_html_user():

    name = request.form['name']
    email = request.form['email']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO users(name, email) VALUES(%s,%s)",
        (name, email)
    )

    mysql.connection.commit()

    return redirect(url_for('home'))

# EDITAR USUARIO HTML
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):

    cur = mysql.connection.cursor()

    # ACTUALIZAR
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        cur.execute(
            """
            UPDATE users
            SET name=%s, email=%s
            WHERE id=%s
            """,
            (name, email, id)
        )

        mysql.connection.commit()

        return redirect(url_for('home'))

    # MOSTRAR FORMULARIO
    cur.execute(
        "SELECT * FROM users WHERE id=%s",
        (id,)
    )

    user = cur.fetchone()

    return render_template('edit.html', user=user)


# ELIMINAR DESDE HTML
@app.route('/delete/<id>')
def delete_html_user(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect(url_for('home'))

# GET USERS
@app.route('/api/users', methods=['GET'])
def get_users():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users")

    data = cur.fetchall()

    users = []

    for row in data:

        users.append({
            'id': row[0],
            'name': row[1],
            'email': row[2]
        })

    return jsonify(users)


# POST USER
@app.route('/api/users', methods=['POST'])
def add_user():

    name = request.json['name']
    email = request.json['email']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO users(name, email) VALUES(%s,%s)",
        (name, email)
    )

    mysql.connection.commit()

    return jsonify({
        'message': 'Usuario agregado'
    })


# PUT USER
@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):

    name = request.json['name']
    email = request.json['email']

    cur = mysql.connection.cursor()

    cur.execute(
        """
        UPDATE users
        SET name=%s, email=%s
        WHERE id=%s
        """,
        (name, email, id)
    )

    mysql.connection.commit()

    return jsonify({
        'message': 'Usuario actualizado'
    })


# DELETE USER
@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    return jsonify({
        'message': 'Usuario eliminado'
    })


if __name__ == "__main__":
    app.run(debug=True)











""" from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL



app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   
app.config['MYSQL_DB'] = 'dbcrud'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users=data)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))
    
@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchall()
        cur.close()
        return render_template('edit.html', user=data[0])
    
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_user(id):    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Index'))

if __name__ == "__main__":    
    app.run(debug=True)   
 """