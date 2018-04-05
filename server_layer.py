# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import json
import pandas as pd
import pickle
import time
from os import listdir, remove

app = Flask(__name__)
API_KEY = "AIzaSyCNEnGoO2oa14kNFjFtEXTHCjt997O44AQ"


@app.route("/",methods=["GET"])
def serverWebPage():
    immostreet = pd.read_csv("appart_zurich_immostreet.csv")
    immostreet.index = immostreet.index.map(str)

    immoscout = pd.read_csv("appart_zurich_immoscout.csv")
    immoscout.index = immoscout.index.map(str)

    homegate = pd.read_csv("appart_zurich_homegate.csv")
    homegate.index = homegate.index.map(str)

    home = pd.read_csv("appart_zurich_home.csv")
    home.index = home.index.map(str)

    return render_template('index.html',
                           flats_immostreet=immostreet.to_dict(orient="index"),
                           flats_immoscout=immoscout.to_dict(orient="index"),
                           flats_homegate=homegate.to_dict(orient="index"),
                           flats_home=home.to_dict(orient="index"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=7070, debug=True)