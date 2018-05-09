#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask,render_template
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route("/")
def index():
    return "ok"


if __name__ == '__main__':
    app.run()
