from flask import Flask,render_template,request

import FeatureExtraction
import pickle

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

app = Flask(__name__)

host_path ='C:\Windows\System32\drivers\etc\hosts'
ip_address = '127.0.0.1'

def Blocker(enter_Website):
    website_lists = enter_Website
    Website = list(website_lists.split(","))
    with open (host_path , 'r+') as host_file:
        file_content = host_file.read()
        for web in Website:
            if web in file_content:
                display='Already Blocked'
                return display
            else:
                host_file.write(ip_address + " " + web + '\n')
                text = "Blocked"
                return text

def Unblock(enter_Website):
    website_lists = enter_Website
    Website = list(website_lists.split(","))
    with open (host_path , 'r+') as host_file:
        file_content = host_file.readlines()
    for web in Website:
            if web in website_lists:
                with open (host_path , 'r+') as f:
                    for line in file_content:
                        if line.strip(',') != website_lists:
                            f.write("\n"+line)
                            text = "UnBlocked"
                            return text
                        else:
                            text = 'Already UnBlocked'
                            return text

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")
    

@app.route('/getURL',methods=['GET','POST'])
def getURL():
    url = request.form['url']
    if request.method == 'POST':
        if not request.form['submit']:
            if request.form['button'] == "Block":
                value = Blocker(url)
                return render_template("home.html",error=value)
            
            if request.form['button'] == "Unblock":
                value = Unblock(url)
                return render_template("home.html",error=value)

        data = FeatureExtraction.getAttributess(url)
        RFmodel = pickle.load(open('RandomForestModel.sav', 'rb'))
        predicted_value = RFmodel.predict(data)
        if predicted_value == 0:    
            value = "Legitimate"
            return render_template("home.html",error=value)
        else:
            value = "Phishing"
            return render_template("home.html",error=value)

if __name__ == "__main__":
    if is_admin():
        # Code of your program here
        app.run(debug=True)
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        app.run(debug=True)