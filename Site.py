from flask import Flask, render_template, url_for, flash, redirect, request
from form import Create
from form2 import Delete
import mysql.connector

#creating an instance of the Flask framework and setting website secret key
app = Flask(__name__)
app.config["SECRET_KEY"] = ("a"*32)

#Creating a MySQL database
db = mysql.connector.connect(host="localhost", user="root", passwd="brightai", database="contactweb ")
mycursor = db.cursor()
#mycursor.execute("CREATE DATABASE contactweb")
#mycursor.execute("CREATE TABLE contacts (First_Name VARCHAR(255), Last_Name VARCHAR(255), Email VARCHAR(255), Phone INTEGER(10))")


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
            mycursor.execute(sql_formula, contact)
            db.commit()

        into_MyDatabase()

        #return redirect(url_for('first_page'))
    return render_template("CreateContact.html", form=form)


@app.route("/contact list")
def second_page():

    #Retrieving the required data from the database
    mycursor.execute("SELECT * FROM contacts")
    info = mycursor.fetchall()
    #mycursor.close()

    return render_template("ContactList.html", contacts=info)

@app.route("/delete contact", methods=["GET", "POST"])
def third_page():
    form2 = Delete()
    if form2.is_submitted():
        required = request.form
        desc1 = str(form2.fn2.data)
        desc2 = str(form2.ln2.data)
        desc3 = str(form2.email2.data)
    if form2.validate_on_submit():
        def outof_MyDatabase():
            contacts = []
            mycursor.execute("SELECT Email FROM contacts")
            info = mycursor.fetchall()

            for contact in info:
                contacts.append(contact)
            if desc3 not in contact:
                flash(f'{form2.fn2.data} {form2.ln2.data}! is not an existing Contact')

            else:
                mycursor.execute("DELETE FROM contacts WHERE First_Name = %s and Last_Name = %s and Email = %s", (desc1, desc2, desc3, ))
                db.commit()
                flash(f'{form2.fn2.data} {form2.ln2.data}! DELETED!', 'success')




        outof_MyDatabase()

    return render_template("DeleteContact.html", form=form2)

if __name__ == "__main__":
    app.run(debug=True)

