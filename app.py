#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for
import config
from get_big_machine_warning import BigWarning
from get_small_machine_warning import SmallWarning

app = Flask(__name__)
app.config.from_object(config)


@app.route("/")
def index():
    big = BigWarning().get_filter_value()
    small = SmallWarning().get_filter_value()
    return render_template("index.html", title="余票预警-测试", bigWarning=big, smallWarning=small)


@app.route("/history/")
def history():
    return render_template("history.html")


@app.route("/kadawo/")
def kadawo():
    return render_template("kadawo.html")


if __name__ == '__main__':
    app.run()
