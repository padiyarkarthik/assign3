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

app = Flask(__name__,template_folder="templates")

import sqlite3
##comment to show
##################
server = 'kpmaster.database.windows.net'
database = 'MySample'
username = 'kpmaster'
password = 'karu@1965'
driver = '{SQL Server}'

cnxn = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                        "Server=tcp:kpmaster.database.windows.net;Database=MySample;Uid=kpmaster;Pwd=karu@1965;")
# cnxn = pyodbc.connect(
#     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

mylist = []

@app.route('/')
def home():
   return render_template('index.php')



@app.route('/cluster')
def cluster():
    return render_template('cluster.html')


@app.route('/UI')
def UI():
    return render_template('view.html')



@app.route('/earthquake')
def earthquake():

   return render_template('view2.html')


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


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    # print("here")

    if request.method == 'POST':
        # print("inside")
        query = "select count(*) from earthquakeus where mag > 5.0"
        print(query)
        cursor.execute(query)
        result=cursor.fetchone()
        print("code here")
        print(result)
        value=result[0]
        print(value)

        return render_template("View.html", msg=value)

@app.route('/search', methods=['GET', 'POST'])
def search():
   if request.method == 'POST':
        range1 = request.form['range1']
        range2 = request.form['range2']
        duration1 = request.form['length']
        if duration1=="day":
            length=datetime.now()-timedelta(days=1)
        if duration1=="week":
            length=datetime.now()-timedelta(days=7)
        if duration1=="month":
            length=datetime.now()-timedelta(days=30)
        cursor.execute("select mag,latitude,longitude from earthquakeus where (mag between "+range1+" and "+range2+") and timee > ?", (length,))
        rows = cursor.fetchall()
        for row in rows:
             print(row)
        return render_template('View.html', rows = rows)



@app.route('/searchTwo', methods=['GET', 'POST'])
def searchTwo():
   if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']


        query=("select top 20 mag,latitude,longitude, place, "
                       "111.045* DEGREES(ACOS(COS(RADIANS(latpoint))"
                       "* COS(RADIANS(latitude))"
                       "* COS(RADIANS(longpoint) - RADIANS(longitude))"
                       "+ SIN(RADIANS(latpoint))"
                       "* SIN(RADIANS(latitude)))) AS distance_in_km "
                       "from earthquakeus "
                       "JOIN ("
                       "SELECT  "+latitude+" AS latpoint, "+longitude+" AS longpoint"
                       ") AS p ON 1=1 "
                       "ORDER BY distance_in_km")
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
             print(row)
        return render_template('view2.html', rows = rows)

@app.route('/searchthree', methods=['GET', 'POST'])
def searchthree():
       if request.method == 'POST':

           value=""
           rangeone = float(request.form['rangeone'])
           rangetwo = float(request.form['rangetwo'])
           query = ("select count(*) from earthquakeus where gap between '"+str(rangeone)+"' and '"+str(rangetwo)+"'")
           print(query)
           cursor.execute(query)
           inBetween = cursor.fetchone()
           print(inBetween)
           value = "In betwen = "+str(inBetween)+" "

           query = ("select count(*) from earthquakeus where gap < '"+str(rangeone)+"'")
           print(query)
           cursor.execute(query)
           below = cursor.fetchone()
           print(below)
           value = value + ", Below = " + str(below) + " "
           print(value)

           query = ("select count(*) from earthquakeus where gap > '" + str(rangetwo) + "'")
           print(query)
           cursor.execute(query)
           above = cursor.fetchone()
           print(above)
           value = value + ", above= " + str(above) + " "
           print(value)


           return render_template('view2.html', rows=value)

# Allow a user, through a web form, to give a location source (locationSource column) such as "us" and
#     a magnitude and then, on a web page, list time, latitude, longitude, and place for all earthquakes larger
#     than that magnitude - ONLY IF the magNst times two is greater than or equal to  the nst (magNst * 2 >= nst).
@app.route('/searchfour', methods=['GET', 'POST'])
def searchfour():
       if request.method == 'POST':


           locationSource = (request.form['locationSource'])
           mag = float(request.form['mag'])

           query = ("select timee,latitude,longitude,place from earthquakeus where locationSource = '"+ locationSource +"' and mag > '"+str(mag)+"'"
                    +" and nst < magNst * 2")
           print(query)
           cursor.execute(query)
           value = cursor.fetchall()
           print(value)
           return render_template('view2.html', rows=value)
# the largest earthquake and smallest earthquake within that distance
#     (please show lat, long, time, and location), as well as showing us the count of total number of earthquakes
#     within that area.
@app.route('/searchfive', methods=['GET', 'POST'])
def searchfive():
   if request.method == 'POST':
        latitude ='32.7357'
        longitude = '-97.1081'
        distancedata = (request.form['distance'])

        query=("select  mag, "
                       "111.045* DEGREES(ACOS(COS(RADIANS(latpoint))"
                       "* COS(RADIANS(latitude))"
                       "* COS(RADIANS(longpoint) - RADIANS(longitude))"
                       "+ SIN(RADIANS(latpoint))"
                       "* SIN(RADIANS(latitude)))) AS distance_in_km "
                       "from earthquakeus "
                       "JOIN ("
                       "SELECT  "+latitude+" AS latpoint, "+longitude+" AS longpoint"
                       ") AS p ON 1=1 "
                       "ORDER BY distance_in_km")
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        count1=0
        temp=0.0
        for i in range(0,len(rows)):
            compare = rows[i]
            check = compare[0]
            checktwo = float(check)
            print(checktwo)
            if(checktwo > temp):
                compare = rows[i]
                check = compare[0]
                checktwo = float(check)
                temp=checktwo

        maxMag = temp
        return render_template('view2.html', rows = temp)

@app.route('/question')
def question():
        query=("select timee from earthquakeus where mag > 4.0")
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        lightmin = datetime(2018, 6, 10, 6, 0, 0).time()
        lightmax = datetime(2018, 6, 10, 20, 0, 0).time()
        countNight=0;
        countDay =0;
        nightmin = datetime(2018, 6, 10, 20, 0, 1).time()
        nightmax = datetime(2018, 6, 10, 23, 59, 59).time()

        for row in rows:
            print(row[0])
            timeInquestion = row[0]
            dataValue = timeInquestion.time()
            print(dataValue)
            if(lightmin<=dataValue<=lightmax):
                countDay=int(countDay)+1
            elif(nightmin<=dataValue<=nightmax):
                countNight = int(countNight) + 1

        print("count of night ")
        print(countNight)
        print("count of day ")
        print(countDay)
        if(countNight>countDay):
            res = 'Yes Night count = ' + str(countNight) +', Day count= ' +str(countDay)
        else:
            res = 'No Night count = ' + str(countNight) +', Day count= ' +str(countDay)

        return render_template('index.php', res = res)



@app.route('/kmeans', methods=['GET', 'POST'])
def main():

        clusters = request.form['clusters']
        K_clusters = int(clusters)
        mylist = getdatafromdatabase()
        cdist=[]
        data = array(mylist)
        cent, pts = kmeans2(data,K_clusters)
        disCluster = []


        for i in range(len(cent)):
            x1 = cent[i][0]
            y1 = cent[i][1]
            x1 = float("{0:.3f}".format(x1))
            y1 = float("{0:.3f}".format(y1))

            ab=(x1,y1)
            for j in range(i+1,len(cent)):
                dc = {}
                x2 = cent[j][0]
                y2 = cent[j][1]
                x2 = float("{0:.3f}".format(x2))
                y2 = float("{0:.3f}".format(y2))
                dist = np.sqrt((x1-x2)*2 + (y1-y2)*2)
                cdist.append(dist)
                dc['dist'] = "Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist)
                disCluster.append(dc)
                print (disCluster)
                print ("Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist))
        clr = ([1, 1, 0.0],[0.2,1,0.2],[1,0.2,0.2],[0.3,0.3,1],[0.0,1.0,1.0],[0.6, 0.6,0.1],[1.0,0.5,0.0],[1.0,	0.0, 1.0],[0.6,	0.2, 0.2],[0.1,0.6,0.6],[0.0,0.0,0.0],[0.8,1.0,1.0],[0.70,0.50,0.50],[0.5,0.5,0.5],[0.77,0.70,0.00])
        colors = ([(clr)[i] for i in pts])
        clr_dict = {"yellow":0,"green":0,"red":0,"blue":0,"cyan":0}
        pdict=[]

        for x in colors:
            if str(x) == "[1, 1, 0.0]":
                clr_dict["yellow"] += 1
            if str(x) == "[0.2, 1, 0.2]":
                clr_dict["green"] += 1
            if str(x) == "[1, 0.2, 0.2]":
                clr_dict["red"] += 1
            if str(x) == "[0.3, 0.3, 1]":
                clr_dict["blue"] += 1
            if str(x) == "[0, 1.0, 1.0]":
                clr_dict["cyan"] += 1
            if str(x) == "[0.6, 0.6,0.1]":
                clr_dict["deepolive"] += 1
            if str(x) == "[1.0,	0.5, 0.0]":
                clr_dict["orange"] += 1
            if str(x) == "[1.0,	0.0, 1.0]":
                clr_dict["magenta"] += 1
            if str(x) == "[0.6,	0.2, 0.2]":
                clr_dict["ruby"] += 1
            if str(x) == "[0.1,	0.6, 0.6]":
                clr_dict["deepteal"] += 1
            if str(x) == "[0.0,	0.0, 0.0]":
                clr_dict["black"] += 1
            if str(x) == "[0.8,	1.0, 1.0]":
                clr_dict["palecyan"] += 1
            if str(x) == "[0.70, 0.50,	0.50]":
                clr_dict["dirtyviolet"] += 1
            if str(x) == "[0.5,	0.5, 0.5]":
                clr_dict["gray"] += 1
            if str(x) == "[0.77, 0.70, 0.00]":
                clr_dict["olive"] += 1


        f_write='Cluster,Count\r\n'
        cnt=0
        print (clr_dict)
        for i in clr_dict:
            if clr_dict[i] == 0:
                continue
            string = str(cnt) + " : " + str(clr_dict[i])
            pdict.append(string)
            print ("No of points in cluster with " + str(i) + " is: " + str(clr_dict[i]))
            f_write+= str(cnt)+','+str(clr_dict[i])+'\r\n'
            cnt += 1
        with open("templates/d3chart.csv",'wb') as nfile:
            nfile.write(f_write.encode("utf-8"))
        plt.scatter(data[:,0],data[:,1], c=colors)
        plt.scatter(cent[:,0],cent[:,1], marker='o', s = 400, linewidths=3, c='none')
        plt.scatter(cent[:,0],cent[:,1], marker='x', s = 400, linewidths=3)

        plt.savefig("static/kmeans6.png")
        plt.gcf().clear("static/kmeans6.png")
        plt.clf()
        plt.cla()
        plt.close()

        return render_template('cluster.html',cdist=cdist,pdict=pdict, disCluster = disCluster)

def getdatafromdatabase():
    query = "select latitude,longitude from earthquakeus"

    print(query)
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        pair=[]
        # print(row)
        # print(row[0])
        # print(row[1])
        x = float(row[0])
        y = float(row[1])
        pair.append(x)
        pair.append(y)
        mylist.append(pair)
    return mylist


@app.route('/show', methods=['GET', 'POST'])
def show():
    print('hit show')
    return render_template('show.html')

@app.route('/Bargraph', methods=['GET', 'POST'])
def bargraph():
  return render_template('d3barchart.html')

@app.route('/Piegraph', methods=['GET', 'POST'])
def Piegraph():
  return render_template('d3piechart.html')


if __name__ == '__main__':
   app.run(debug = True)