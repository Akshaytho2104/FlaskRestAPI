from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, validators, StringField, FloatField, IntegerField, DateField, SelectField
from datetime import datetime
import MySQLdb
import urllib
import requests

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] ="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="users"
app.config["MYSQL_PORT"]=3306
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql=MySQL(app)

@app.route("/")
def index():
    return render_template("home.html")

# Users
@app.route("/Students")
def Students():
    cur=mysql.connection.cursor()

    # Execute SQL query

    result = cur.execute("SELECT * From Students")
    Students = cur.fetchall()

    # Render Template
    if result>0:
        return render_template("Students.html",Students=Students)
    else:
        msg="No Students Found"
        return render_template("Students.html",warning=msg)
    cur.close()

# View Details of Students by ID
@app.route('/Students/<string:id>')
def viewStudents(id):
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    result = cur.execute("SELECT * FROM Students WHERE id=%s", [id])
    Students = cur.fetchone()

    # Render Template
    if result > 0:
        return render_template('view_Students_details.html', Students=Students)
    else:
        msg = 'This Students Does Not Exist'
        return render_template('view_Students_details.html', warning=msg)

    # Close DB Connection
    cur.close()


# Define Add-Students-Form
class AddStudents(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    Age = IntegerField('Age', [validators.NumberRange(min=6, max=50)])
    City = StringField('City', [validators.length(min=2)])




# Add Students
@app.route('/add_Students', methods=['GET', 'POST'])
def add_Students():
    # Get form data from request
    form = AddStudents(request.form)

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        Age = form.Age.data
        City = form.City.data



        # Create MySQLCursor
        cur = mysql.connection.cursor()

        # Execute SQL Query
        cur.execute(
            "INSERT INTO Students (name,email,Age, City ) VALUES (%s,%s,%s,%s)", (name, email,Age,City))

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("New Students Added", "success")

        # Redirect to show all Students
        return redirect(url_for('Students'))

    # To handle GET request to route
    return render_template('add_Students.html', form=form)


# Edit Students by ID
@app.route('/edit_Students/<string:id>', methods=['GET', 'POST'])
def edit_Students(id):
    # Get form data from request
    form = AddStudents(request.form)

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        Age = form.Age.data
        City = form.City.data


        # Create MySQLCursor
        cur = mysql.connection.cursor()

        # Execute SQL Query
        cur.execute(
            "UPDATE Students SET name=%s, email=%s ,Age=%s,City=%s WHERE id=%s", (name, email,Age,City, id))

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("Students Updated", "success")

        # Redirect to show all Students
        return redirect(url_for('Students'))

    # To handle GET request to route

    # To get existing field values of selected Students
    cur2 = mysql.connection.cursor()
    result = cur2.execute("SELECT name,email,Age,City FROM Students WHERE id=%s", [id])
    Students = cur2.fetchone()
    # To render edit Students form
    return render_template('edit_Students.html', form=form, Students=Students)


# Delete Students by ID
# Using POST instead of DELETE because HTML form can only send GET and POST requests
@app.route('/delete_Students/<string:id>', methods=['POST'])
def delete_Students(id):

    # Create MySQLCursor
    cur = mysql.connection.cursor()
    # Since deleting parent row can cause a foreign key constraint to fail
    try:
        # Execute SQL Query
        cur.execute("DELETE FROM Students WHERE id=%s", [id])

        # Commit to DB
        mysql.connection.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # Flash Failure Message
        flash("Students could not be deleted", "danger")
        flash(str(e), "danger")

        # Redirect to show all Students
        return redirect(url_for('Students'))
    finally:
        # Close DB Connection
        cur.close()

    # Flash Success Message
    flash("Students Deleted", "success")

    # Redirect to show all Students
    return redirect(url_for('Students'))

if __name__ == '__main__':
    app.secret_key = "secret"
    app.run(debug=True)


