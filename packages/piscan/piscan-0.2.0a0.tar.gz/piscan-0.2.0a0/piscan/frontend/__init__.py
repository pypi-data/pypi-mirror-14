from flask import Flask, redirect, url_for, request, render_template, Markup
import time, sys, subprocess
from sh import tail

app = Flask(__name__)

@app.route("/")
def hello():
    #return render_template('index.html', item='Here!')
    return ("Ooooh... I see...")


@app.route("/logs/piqueue")
def piqueuelogs():
    #return render_template('index.html', item='Here!')
    logfile = r"/var/log/piqueue.log"
    logs = ""
    file = open(logfile, 'rU')
    logs = file.read()
    logs = logs[-4000:]
    logs = logs.replace('\n', '<br>')
    return render_template('index.html', item=Markup(logs))

@app.route("/logs/pirec")
def pireclogs():
    #return render_template('index.html', item='Here!')
    logfile = r"/var/log/pirec.log"
    logs = ""
    file = open(logfile, 'rU')
    logs = file.read()
    logs = logs[-4000:]
    logs = logs.replace('\n', '<br>')
    return render_template('index.html', item=Markup(logs))





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

 
