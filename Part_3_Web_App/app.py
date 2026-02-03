import os
import smtplib
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"  
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get credentials securely
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

def calculate_topsis(file_path, weights, impacts):
    try:
        df = pd.read_csv(file_path)
        
        if df.shape[1] < 3:
            return None, "Input file must contain 3 or more columns."

        # Check for non-numeric columns (from 2nd column onwards)
        data = df.iloc[:, 1:].values
        try:
            data = data.astype(float)
        except ValueError:
            return None, "Columns from 2nd to last must contain numeric values only."

        w = np.array([float(x) for x in weights.split(',')])
        imp = impacts.split(',')

        if len(w) != data.shape[1] or len(imp) != data.shape[1]:
            return None, "Weights/Impacts length mismatch."

        if not all(i in ['+', '-'] for i in imp):
            return None, "Impacts must be '+' or '-'."

        # Normalize
        rss = np.sqrt(np.sum(data**2, axis=0))
        rss[rss == 0] = 1
        norm = data / rss
        weighted = norm * w

        best, worst = [], []
        for i in range(len(imp)):
            if imp[i] == '+':
                best.append(np.max(weighted[:, i]))
                worst.append(np.min(weighted[:, i]))
            else:
                best.append(np.min(weighted[:, i]))
                worst.append(np.max(weighted[:, i]))

        s_best = np.sqrt(np.sum((weighted - np.array(best))**2, axis=1))
        s_worst = np.sqrt(np.sum((weighted - np.array(worst))**2, axis=1))
        
        score = s_worst / (s_best + s_worst)
        
        df['Topsis Score'] = score
        df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
        
        output_filename = 'result_' + os.path.basename(file_path)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        df.to_csv(output_path, index=False)
        return output_path, None

    except Exception as e:
        return None, str(e)

def send_email(to_email, filename):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Result"
    
    body = "Please find attached the result of your TOPSIS analysis."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename=result.csv")
        msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'datafile' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
            
        file = request.files['datafile']
        weights = request.form.get('weights')
        impacts = request.form.get('impacts')
        email = request.form.get('email')
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            result_path, error = calculate_topsis(filepath, weights, impacts)
            
            if error:
                flash(f"Error: {error}")
                os.remove(filepath)
            else:
                if send_email(email, result_path):
                    flash(f"Success! Result sent to {email}")
                else:
                    flash("Error sending email. Check credentials.")
                
                # Cleanup
                if os.path.exists(filepath): os.remove(filepath)
                if os.path.exists(result_path): os.remove(result_path)
                
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)