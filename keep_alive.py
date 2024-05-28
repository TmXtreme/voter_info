from flask import Flask, redirect, send_from_directory
from threading import Thread

app = Flask(__name__)

# Add a route for serving favicon.ico
@app.route('/favicon.ico')
def favicon():
    return redirect('https://raw.githubusercontent.com/TmXtreme/Xtreme-info/main/favicon.ico')


@app.route('/')
def index():
    return "Alive"

def run():
    app.run(host='0.0.0.0', port=8089)

def keep_alive():
    t = Thread(target=run, name="FlaskThread")
    t.start()

if __name__ == "__main__":
    keep_alive()