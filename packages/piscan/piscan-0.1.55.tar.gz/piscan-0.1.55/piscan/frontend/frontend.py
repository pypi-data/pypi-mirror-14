import subprocess
from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/logs/<log>')
def logs(log=None):
    return render_template('logs.html', log=log)

@app.route('/status')
def status():
    p = subprocess.Popen(["service", "pirec", "status"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    p = subprocess.Popen(["service", "piqueue", "status"], stdout=subprocess.PIPE)
    out2, err = p.communicate()
    out = out[46:] + "<br>" + out2[46:]
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
