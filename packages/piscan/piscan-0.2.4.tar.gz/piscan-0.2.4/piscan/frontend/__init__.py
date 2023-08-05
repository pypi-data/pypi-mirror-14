from flask import Flask, redirect, url_for, request, render_template, Markup
import time, sys, subprocess, pika, os, subprocess
from sh import tail

app = Flask(__name__)

@app.route("/")
def hello():
    htmlcode = ''
    connection = pika.BlockingConnection()
    channel = connection.channel()
    q = channel.queue_declare("LameQ")
    q_len = q.method.message_count


    p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    if ('pirec' in out):
        htmlcode = htmlcode + "PiRec is running<br>"
    if ('piqueue' in out):
        htmlcode = htmlcode + "PiQueue is running<br>"
    if ('rabbitmq' in out):
        htmlcode = htmlcode + "RabbitMQ is running<br>"

    htmlcode = htmlcode + "There are " + str(q_len) + " messages in the local queue"

    return render_template('index.html', item=Markup(logs))



@app.route("/logs")
def piqueuelogs():
    htmlcode="<A href='/logs/pirec'>PiRec Logs</a><br><A href='/logs/piqueue'>PiQueue Logs</a>"
    return render_template('index.html', item=Markup(htmlcode))


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

 
