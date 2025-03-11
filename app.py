from flask import Flask, render_template, request, redirect, url_for, session
from predict import model_prediction
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import yagmail


app = Flask(__name__)
app.secret_key = "cyberbullying"


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pwd"]
        pwd = str(pwd)
        print("pwd : ", pwd)
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):
                session['email'] = email  
                return redirect(url_for('home'))

        mesg = 'Invalid Login Try Again'
        return render_template('login.html', msg=mesg)
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            email = request.form['email']
            pwd = request.form['pwd']
            repwd = request.form['repwd']
            if pwd == repwd:  # Fix the comparison operator
                col_list = ["email", "password"]
                try:
                    r1 = pd.read_excel('user.xlsx', usecols=col_list)
                except FileNotFoundError:
                    r1 = pd.DataFrame(columns=col_list)

                new_row = pd.DataFrame({'email': [email], 'password': [pwd]})
                r1 = pd.concat([r1, new_row], ignore_index=True)

                r1.to_excel('user.xlsx', index=False)
                print("Records created successfully")
                msg = 'Registration Successful. You can log in here.'
                return render_template('login.html', msg=msg)
            else:
                msg = 'Password and Re-enter password do not match.'
                return render_template('register.html', msg=msg)
        return render_template('register.html')
    except Exception as e:
        return render_template('register.html', msg=e)
     


@app.route("/home")
def home():   
    if 'email' in session:
        return render_template("index.html")
    else:
        return render_template('login.html')


def sendmail(result, user_mails, input_text):  
    try:
        yag = yagmail.SMTP(user='krishnareddys069@gmail.com', password='gygwzouinhkpjnuc')
        solution = "If you encounter cyberbullying, consider reporting it to the platform, blocking the offender, and seeking help from trusted individuals or authorities."

        for user_mail in user_mails:
            mail_contents = [
                f"Classification Result: {result}.\n\n\n",
                f"User Input Text: {input_text}\n\n",
                f"Suggested Action: {solution}\n\n"
            ]
            yag.send(to=user_mail, subject=f"{result} related Cyber Bullying Detected", contents=mail_contents)

        print('[SUCCESS]  > Email sent successfully...')
        return "success"
    except Exception as e:
        print('[FAILED]    >', e)
        return "failed"


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        email_id = session['email']
        prediction = "Not-Cyberbullying"
        msg = ""

        if request.method == 'POST':
            text_file = request.form['text_file']
            print(f'text_file : {text_file}')
        
            prediction = model_prediction(text_file)

            if prediction == "Cyberbullying":
                mail_status = sendmail(prediction, user_mails=[email_id], input_text=text_file)
                if mail_status == "success":
                    msg = f"Alert: Cyberbullying detected. Email sent to {email_id}."
                else:
                    msg = f"Failed to send email alert to {email_id}."
            else:
                msg = "No cyberbullying detected."

        return render_template('index.html', pro=prediction, msg=msg, input_text=text_file)

    else:
        return redirect(url_for('login'))
        

@app.route('/password', methods=['POST', 'GET'])
def password():
    if 'email' in session:    
        if request.method == 'POST':
            current_pass = request.form['current']
            new_pass = request.form['new']
            verify_pass = request.form['verify']
            r1 = pd.read_excel('user.xlsx')
            for index, row in r1.iterrows():
                if row["password"] == str(current_pass):
                    if new_pass == verify_pass:
                        r1.loc[index, "password"] = verify_pass
                        r1.to_excel("user.xlsx", index=False)
                        msg1 = 'Password changed successfully'
                        return render_template('password.html', msg=msg1)
                    else:
                        msg = 'Re-entered password is not matched'
                        return render_template('password.html', msg=msg)
            else:
                msg3 = 'Incorrect Password'
                return render_template('password.html', msg=msg3)
        return render_template('password.html')
    else:
        return redirect(url_for('login'))


@app.route("/graph")
def graph():
    if 'email' in session:
        return render_template("graphs.html")
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove email from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5005)
