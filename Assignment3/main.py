from flask import Flask, render_template, request, redirect, url_for, send_from_directory

#import sqlite3 as sql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import uuid
from numpy import vstack, array
from scipy.cluster.vq import *
from datetime import datetime
from datetime import timedelta
import csv
import os
import pypyodbc
# import pyodbc


#import sqlite3
##comment to show
#test
#server = 'kpmaster.database.windows.net'
#database = 'earthquakeus'
#username = 'kpmaster'
#password = 'karu@1965'
#driver = '{SQL Server}'

cnxn = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                        "Server=tcp:kpmaster.database.windows.net;Database=MySample;Uid=kpmaster;Pwd=karu@1965;")
# cnxn = pyodbc.connect(
#     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.php')




@app.route('/uploadCSV',methods=['POST'])
def uploadCSV():
    file = request.files['file']
    print(file.filename)
    #######
    destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    newfiledest = "/".join([destination, file.filename])
    file.save(newfiledest)
    #######
    with open(file.filename, encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        columns = next(reader)
        print(columns)
        query = 'insert into earthquakeus ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            cursor.execute(query, data)
            cursor.commit()

        m = os.path.getsize(newfiledest)

        return render_template('index.php', variable=m)


if __name__ == '__main__':
   app.run(debug = True)