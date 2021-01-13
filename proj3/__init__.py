from flask import Flask, render_template, url_for, request

app=Flask(__name__)

@app.route('/')
def home():
    #return render_template('home.html',imgurl="{{ url_for('static',filename='images/title0.svg') }}")
    return render_template('index.html')

@app.route('/dash')
def dash():
    return render_template('dash.html')

app.run(use_reloader=False, port='800')