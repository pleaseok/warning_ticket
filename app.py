#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/history/")
def history():
    return render_template("history.html")

@app.route("/kadawo/")
def kadawo():
    return render_template("kadawo.html")

if __name__ == '__main__':
    app.run()
