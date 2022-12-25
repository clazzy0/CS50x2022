import requests
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, after_this_request, make_response

def error(message, code=400):
    return render_template("error.html", top=code, bottom=message.upper()), code