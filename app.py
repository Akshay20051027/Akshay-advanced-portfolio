from flask import Flask, render_template, request, jsonify

import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
import os



app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Your HTML file name

@app.route('/send_contact', methods=['POST'])
def send_contact():
    data = request.json
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    user_message = data.get('message', '')
    contact_methods = data.get('contact_methods', {})  # {email: bool, whatsapp: bool}

    thank_you_msg = (
        f"Hello {name}!\n\n"
        f"Thank you for contacting Akshay GupthA.\n\n"
        f"We received your message:\n\"{user_message}\"\n\n"
        f"Akshay will get back to you shortly regarding your inquiry.\n\n"
        f"Best regards,\n"
        f"Akshay GupthA Portfolio Team"
    )

    results = {
        "whatsapp": "Not selected",
        "email": "Not selected"
    }
    results["whatsapp"] = "WhatsApp automation not supported in cloud."
    # Send WhatsApp message
    '''if contact_methods.get('whatsapp', False) and phone:
        try:
            # Clean phone number
            phone_clean = ''.join(filter(str.isdigit, phone))
            if not phone_clean.startswith('91') and len(phone_clean) == 10:
                phone_clean = '91' + phone_clean
            full_number = '+' + phone_clean
            time.sleep(5)
            time.sleep(5)
            print(f"Sending WhatsApp to {full_number}")
            pwk.sendwhatmsg_instantly(full_number, thank_you_msg, wait_time=15, tab_close=True)
            time.sleep(10)
            pyautogui.press("enter")
            results["whatsapp"] = "Message sent successfully!"
        except Exception as e:
            print("WhatsApp error:", e)
            results["whatsapp"] = f"Failed to send: {str(e)}"'''

    # Send Email message
    if contact_methods.get('email', False) and email:
        try:
            sender_email = "aakshayguptha@gmail.com"         # <-- Replace with your sender
            sender_password = "wcba yrca rswq kkzy"          # <-- Use Gmail App Password

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "Thank you for contacting Akshay GupthA"
            msg.attach(MIMEText(thank_you_msg, 'plain'))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            results["email"] = "Email sent successfully!"
        except Exception as e:
            print("Email error:", e)
            results["email"] = f"Failed to send: {str(e)}"

    return jsonify({
        "message": "Your message has been received!",
        "results": results
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(debug=False, host='0.0.0.0', port=port)  # Allow external access
