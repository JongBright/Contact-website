from flask import Flask, render_template, url_for, flash, redirect, request
from form import Create
import mysql.connector
from flask_mysqldb import MySQL



#creating an instance of the Flask framework and setting website secret key
app = Flask(__name__)
app.config["SECRET_KEY"] = ("a"*32)

#Initializing MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'brightai'
app.config['MYSQL_DB'] = 'contactweb'

db = MySQL(app)


#routing the website pages
@app.route("/", methods=["GET", "POST"])
def first_page():

    form = Create()
    if form.is_submitted():
        required = request.form
    if form.validate_on_submit():
        flash(f'{form.fn.data} {form.ln.data}! ADDED SUCCESFULLY!', 'success')

        #Populating the contact database for storing the contacts
        def into_MyDatabase():

            temp = []
            for value in required.values():
                if len(value)<30 and value!="Done":
                    temp.append(value)
            contact = tuple(temp)

            #Creating a table to store gotten data from the website to the database
            sql_formula = "INSERT INTO contacts (First_Name, Last_Name, Email, Phone) VALUES (%s, %s, %s, %s)"
            mycursor = db.connection.cursor()
            mycursor.execute(sql_formula, contact)
            db.connection.commit()

        into_MyDatabase()

    return render_template("CreateContact.html", form=form)

@app.route("/contact list")
def second_page():

    #Retrieving the required data from the database
    mycursor = db.connection.cursor()
    mycursor.execute("SELECT * FROM contacts")
    info = mycursor.fetchall()
    #mycursor.close()

    return render_template("ContactList.html", contacts=info)



@app.route("/delete contact/<string:id>", methods=["GET", "POST"])
def third_page(id):

    mycursor = db.connection.cursor()
    mycursor.execute('DELETE FROM contacts WHERE Email = (%s) ', (id, ))
    db.connection.commit()

    return redirect(url_for('second_page'))


@app.route("/edit contact/<string:id>", methods=["GET", "POST"])
def fourth_page(id):

    mycursor = db.connection.cursor()
    mycursor.execute("SELECT * FROM contacts WHERE Email = (%s)", (id, ))
    info = mycursor.fetchall()

    return render_template("UpdateContact.html", contact=info[0])


@app.route("/update contact/<string:id>", methods=["POST", "GET"])
def fifth_page(id):

    #Getting data from the edit form
    if request.method == 'POST':
            f_name = request.form['First_Name']
            l_name = request.form['Last_Name']
            email = request.form['Email']
            tel = request.form['Phone']

    #Applying the contact update using the gotten data
            mycursor = db.connection.cursor()
            mycursor.execute("""
            UPDATE contacts
            SET First_Name = %s, Last_Name = %s, Email = %s, Phone = %s
            WHERE Email = %s


            """, (f_name, l_name, email, tel, id))

            db.connection.commit()
            #flash(f'Contact UPDATED successfully!', 'success')


    return redirect(url_for('second_page'))



if __name__ == "__main__":
    app.run(debug=True)

