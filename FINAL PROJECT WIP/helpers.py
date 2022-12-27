import requests
import os
from flask import Flask, render_template

def error(message, code=400):
    return render_template("error.html", top=code, bottom=message.upper()), code
