from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import secrets
import smtplib
from blockchain import *
from collections import defaultdict
import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="medicalstorage",
    charset='utf8',
    port=3306
)
mycursor = mydb.cursor()

# Serializer for generating confirmation tokens
s = URLSafeTimedSerializer(app.secret_key)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for registration
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['Con_Password']
        email = request.form['email']
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']
        security_question1 = request.form['security_question1']
        security_answer1 = request.form['security_answer1']
        security_question2 = request.form['security_question2']
        security_answer2 = request.form['security_answer2']
        role = request.form['role']
        institution = request.form['institution']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()

        if password == password1:
            print(password)
            sql = "SELECT * FROM users WHERE email = %s AND password = %s"
            mycursor.execute(sql, (email, hashpassword))
            data = mycursor.fetchall()
            print(data)

            print(username, email, password)
            sql = """
            INSERT INTO users (username, password, email, full_name, phone, address, security_question1, security_answer1, security_question2, security_answer2, role, institution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (username, hashpassword, email, full_name, phone, address, security_question1, security_answer1, security_question2, security_answer2, role, institution)
            mycursor.execute(sql, val)
            mydb.commit()

            # Prepare data for Excel
            data = {
                'Username': [username],
                'Email': [email],
                'Full Name': [full_name],
                'Phone': [phone],
                'Address': [address],
                'Security Question 1': [security_question1],
                'Security Answer 1': [security_answer1],
                'Security Question 2': [security_question2],
                'Security Answer 2': [security_answer2],
                'Role': [role],
                'Institution': [institution],
            }
            df = pd.DataFrame(data)

            # Check if the Excel file exists
            excel_file = 'registration_data.xlsx'
            if os.path.exists(excel_file):
                # If it exists, append without headers
                with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            else:
                # If it doesn't exist, create a new file
                df.to_excel(excel_file, index=False)

            # Email verification logic (pseudo-code)
            token = s.dumps(email, salt='email-confirm')
            link = url_for('confirm_email', token=token, _external=True)
            # Send the link to the user's email address (implement email sending logic)
            flash('A confirmation email has been sent to you by email.', 'info')
            return redirect(url_for('login'))
    return render_template('register.html')



# Route to confirm email
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    sql = "UPDATE users SET is_verified = %s WHERE email = %s"
    val = (True, email)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Your account has been verified.', 'success')
    return redirect(url_for('login'))

# Route for login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        sql = "select * from users where email='%s' and password='%s'" % (email, hashpassword)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if results != []:
            # session['username'] = username
            session['email'] = email
            flash("Login Successfull","Success")
            return render_template('userhome.html',data=results)
        else:
            flash("Credential's Doesn't Exist","warning")
            return render_template('login.html',)        
    return render_template('login.html',) 

@app.route("/userhome")  
def userhome():
    return render_template('userhome.html')

@app.route("/MCSShome")  
def MCSShome():
    return render_template('MCSShome.html')

@app.route("/tpahome")  
def tpahome():
    return render_template('tpahome.html')


@app.route("/MShome")  
def MShome():
    return render_template('MShome.html')


#Third-Party Auditor  login
@app.route("/tpa", methods=["POST", "GET"])
def tpa():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'tpa@gmail.com' and password == 'tpa':
            return render_template('tpahome.html', msg="Login successfull")
        else:
            return render_template('tpa.html', msg="Login Failed!!")
    return render_template('tpa.html')


#Medical Cloud Storage Server  login
@app.route("/MCSS", methods=["POST", "GET"])
def MCSS():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'MCSS@gmail.com' and password == 'MCSS':
            return render_template('MCSShome.html', msg="Login successfull")
        else:
            return render_template('MCSS.html', msg="Login Failed!!")
    return render_template('MCSS.html')

#Medical Staff login
@app.route("/medical", methods=["POST", "GET"])
def medical():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'MS@gmail.com' and password == 'MS':
            return render_template('MShome.html', msg="Login successfull")
        else:
            return render_template('MS.html', msg="Login Failed!!")
    return render_template('MS.html')

@app.route("/UploadFiles", methods=['POST', 'GET'])
def UploadFiles():
    if request.method == 'POST':
        patirntname = request.form['patientname']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']
        temperature = request.form['temperature']
        respiratory = request.form['respiratory']
        pulserate = request.form['pulserate']
        motion = request.form['motion']
        hydration = request.form['hydration']
        gas = request.form['gas']
        glucose = request.form['glucose']
        FileName = request.form['FileName']
        Keywords = request.form['Keywords']
        Files = request.files['Files']
        
        # Ensure the filename is secure
        n = secure_filename(Files.filename)
        path = os.path.join("uploads/", n)
        Files.save(path)
        
        # Read the file content
        dd = r"uploads/" + n
        with open(dd, "r") as f:
            data = f.read()
        
        # Check if the FileName or Keywords already exist in the database
        sql = "SELECT FileName, Keywords FROM filesupload WHERE FileName=%s OR Keywords=%s"
        mycursor.execute(sql, (FileName, Keywords))
        existing_records = mycursor.fetchall()
        
        if existing_records:
            flash(f"A record with FileName '{FileName}' or Keywords '{Keywords}' already exists.", "danger")
            return render_template('UploadFiles.html')
        
        # Insert new data into the database
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        
        sql = """INSERT INTO filesupload 
                 (doemail, patirntname, age, contact, address, temperature, respiratory, pulserate, motion, hydration, gas, glucose, FileName, Keywords, Files, DateTime) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, AES_ENCRYPT(%s,'rupesh'), %s)"""
        values = (session['email'], patirntname, age, contact, address, temperature, respiratory, pulserate, motion, hydration, gas, glucose, FileName, Keywords, data, current_datetime)
        mycursor.execute(sql, values)
        mydb.commit()
        
        # Create an Excel sheet with the uploaded data
        df = pd.DataFrame({
            "Patient Name": [patirntname],
            "Age": [age],
            "Address": [address],
            "Contact": [contact],
            "Temperature": [temperature],
            "Respiratory": [respiratory],
            "Pulse Rate": [pulserate],
            "Motion": [motion],
            "Hydration": [hydration],
            "Gas": [gas],
            "Glucose": [glucose],
            "File Name": [FileName],
            "Keywords": [Keywords],
            "DateTime": [current_datetime]
        })
        excel_path = os.path.join("uploads/", f"{FileName}.xlsx")
        df.to_excel(excel_path, index=False)
        
        return render_template("UploadFiles.html", msg="success", files=Files)
    
    return render_template("UploadFiles.html")

#view my uploaded files
@app.route('/viewmyfile')
def viewmyfile():
    sql="select * from filesupload where doemail='%s' "%(session['email'])
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('viewmyfile.html',data=data)

# accept data receiver request
@app.route("/generatekey/<id>")
def generatekey(id):
    # Generate an 8-character secure key
    key = secrets.token_urlsafe(6)  # 8-character key, URL-safe
    
    # Update the record with the generated key
    sql_update = "UPDATE filesupload SET Secratekey=%s WHERE id=%s"
    kdata= mycursor.execute(sql_update, (key, id))
    mydb.commit()
    print(key,kdata)
    
    # Flash a success message
    flash('Key updated successfully', 'success')
    
    # Redirect to the viewmyfile page
    return redirect(url_for('viewmyfile'))


@app.route('/taggen')
def taggen():
    sql="select * from filesupload where doemail='%s' "%(session['email'])
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('taggen.html', data=data)

@app.route("/tagname/<id>")
def tagname(id):
    print(id)
    # Generate an 8-character secure key
    # key = secrets.token_urlsafe(6)  # 8-character key, URL-safe
    
    # # Update the record with the generated key
    # sql_update = "UPDATE filesupload SET Tagname=%s WHERE id=%s"
    # mycursor.execute(sql_update, (key, id))
    # mydb.commit()
    # print(key)
    
    # # Flash a success message
    # flash('Key updated successfully', 'success')
    
    # Redirect to the viewmyfile page
    return render_template('tagname.html', id=id)

@app.route('/add_tag/<int:id>', methods=['POST'])
def add_tag(id):
    tag_name = request.form['tag_name']
    sql = "UPDATE filesupload SET Tagname=%s WHERE id=%s"
    mycursor.execute(sql, (tag_name, id))
    mydb.commit()
    flash('Tag added successfully', 'success')
    return redirect(url_for('taggen'))

@app.route('/viewallfile')
def viewallfile():
    sql="select * from filesupload "
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('viewallfile.html',data=data)

@app.route('/filerequest/<id>')
def filerequest(id=0):
    sql="select * from filesupload where Id='%s'"%(id)
    x=pd.read_sql_query(sql,mydb)
    print(x)
    print("**********")
    id = x.values[0][0]
    doemail = x.values[0][1]
    patirntname =x.values[0][2]
    age = x.values[0][3]
    contact = x.values[0][4]
    address = x.values[0][5]
    temperature =x.values[0][6]
    respiratory =x.values[0][7]
    pulserate = x.values[0][8]
    motion = x.values[0][9]
    hydration =x.values[0][10]
    gas =x.values[0][11]
    glucose = x.values[0][12]
    FileName = x.values[0][13]
    Keywords =x.values[0][17]
    Files =x.values[0][18]
    Secratekey = x.values[0][14]
    Tagname = x.values[0][15]
    pemail = session['email']
    status = 'Requested'
    print("******************")
    print(id,doemail,patirntname,age,contact,address,temperature,respiratory,pulserate,motion,hydration,gas,glucose,FileName,Keywords,Files,Secratekey,Tagname,pemail,status )
    mydb.commit()
    otp = random.randint(000000, 999999)

    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    print(999999999999,current_datetime)

    # Insert request into database
    sql = "INSERT INTO filerequest (FileId,doemail,patirntname,age,contact,address,temperature,respiratory,pulserate,motion,hydration,gas,glucose,FileName,Keywords,Files,Secratekey,Tagname,pemail,OTP,status,Requestedtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"
    val = (id,doemail,patirntname,age,contact,address,temperature,respiratory,pulserate,motion,hydration,gas,glucose,FileName,Keywords,Files,Secratekey,Tagname,pemail,otp,status,current_datetime)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Request sent successfully.', 'success')
    return redirect('/viewallfile')

@app.route("/viewfile/<id>")
def viewfile(id):
    print(id)
    sql = "SELECT * FROM filerequest WHERE id = %s"
    data = pd.read_sql_query(sql, mydb, params=[id])
    print(data)

    return render_template('viewfile.html', dat=data)

@app.route("/enterkey/<id>", methods=['POST', 'GET'])
def enterkey(id):
    print("*****************")
    print(id)
    return render_template("enterkey.html", id=id)


@app.route("/key",methods=["POST","GET"])
def key():
    if request.method=='POST':
        file=request.form["pkey"]
        print(file)
        
        sql=f"select AES_DECRYPT(Files,'rupesh') from filerequest where pemail ='{session['email']}' and  Verification='Verified' and OTP={file}"
        data=pd.read_sql_query(sql,mydb)
        print('=========================================================')
        print(data.values[0][0])
        mydb.commit()
        print(99999999999,data)
        # data=pd.read_sql_query(sql)
        return render_template("key.html",row_val=[[data.values[0][0]]])
        # except:
        #     return render_template("key.html",msg="notfound")
    return render_template("key.html")

@app.route("/filedownload/<int:id>")
def filedownload(id=0):
    print(id)
    return render_template("filedownload.html")


@app.route('/viewfilebymcss')
def viewfilebymcss():
    sql="select * from filesupload "
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('viewfilebymcss.html',data=data)

@app.route('/viewfilerequest')
def viewfilerequest():
    sql="select * from filerequest where status='Requested'"
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('viewfilerequest.html',data=data)


# accept data receiver request
@app.route("/accept_request/<id>")
def accept_request(id=0):
    print(id)
    sql = "select * from filerequest where status='Requested'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)

    
    sql = "update filerequest set status='Accepted' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('File Requested Accepted successfully.', 'success')
    return redirect(url_for('viewfilerequest'))

# reject data receiver request
@app.route("/reject_request/<id>")
def reject_request(id=0):
    print(id)
    sql = "select * from filerequest where status='Requested'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
   
    sql = "update filerequest set status='Rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('File Requested Rejected successfully.', 'success')
    return redirect(url_for('viewfilerequest'))

@app.route('/responsetoaudit')
def responsetoaudit():
    sql="select * from filerequest where status='Accepted' and Verification='Sentdata'"
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('responsetoaudit.html',data=data)

@app.route('/auditrequest')
def auditrequest():
    sql="select * from filerequest where status='Accepted'"
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('auditrequest.html',data=data)



# accept data receiver request
@app.route("/accept_verification/<id>")
def accept_verification(id=0):
    print(id)
    sql = "select * from filerequest where Verification='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)

    
    sql = "update filerequest set Verification='Verified' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()

    sql = "update filesupload set Verification='Verified' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('File Verification Accepted successfully.', 'success')
    return redirect(url_for('auditrequest'))

# reject data receiver request
@app.route("/reject_verification/<id>")
def reject_verification(id=0):
    print(id)
    sql = "select * from filerequest where Verification='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
   
    sql = "update filerequest set Verification='VerificationFailed' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('File Verification Failed or not Accepted successfully.', 'success')
    return redirect(url_for('auditrequest'))

@app.route('/verifyproofe')
def verifyproofe():
    sql="select * from filerequest where Verification='Verified'"
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('verifyproofe.html',data=data)

@app.route('/patientdata')
def patientdata():
    sql="select * from filerequest where Verification='Verified'"
    data=pd.read_sql_query(sql,mydb)
    mydb.commit()
    print(data)
    return render_template('patientdata.html',data=data)

@app.route("/Sendkey/<id>")
def Sendkey(id=0):
    sql="select * from filerequest where id='%s'"%(id)
    x=pd.read_sql_query(sql,mydb)
    print(x)
    print("**********")
    id = x.values[0][0]
    doemail = x.values[0][1]
    OTP =x.values[0][20]
    pemail =x.values[0][19]
    
    print(22222,OTP,pemail)
   
    sender_address = 'bhargavvarmavellasiri@gmail.com'
    sender_pass = 'aupslbxqjkzizppq'
    receiver_address = pemail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message.attach(MIMEText(OTP, 'plain'))
    abc = smtplib.SMTP('smtp.gmail.com', 587)
    abc.starttls()
    abc.login(sender_address, sender_pass)
    text = message.as_string()
    abc.sendmail(sender_address, receiver_address, text)
    abc.quit()
    
    flash('Key Transfered To user through email.', 'success')
    return redirect(url_for('patientdata'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
