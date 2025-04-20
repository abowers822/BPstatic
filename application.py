# Implements a registration form, storing registrants in a SQLite database
import os
import re
import datetime
import pymysql
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message

application = Flask(__name__)

application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'abowers822@gmail.com'
application.config['MAIL_PASSWORD'] = '$SAwe8123**'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)

MONTHS = [
    "CURRENT",
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
    "ALL"
]

MFGS = [
    "Pfizer",
    "Moderna",
    "Jenssen"
]




@application.route("/")
def dbrecord():
    return render_template("bp.html")
@application.route("/bpview")
def bpview():
    return render_template("bpview.html",months=MONTHS)

@application.route("/bpregistrants", methods=["POST"])
def bpregistrants():
    name = request.form.get("name")
    month = request.form.get("month")
    
    if not name:
        return render_template("failure.html")
    conn=pymysql.connect(
        host="frosh.cobqsqo3tc26.us-east-1.rds.amazonaws.com",
        user="abowers822",
        password="$Sawe8123*",
        db="new_schema"
    )
    wherestr=""
    cur=conn.cursor()
    if month == "ALL":
        wherestr = "where name like \'%s\';"%name
    elif month == "CURRENT":
        x = datetime.datetime.now()
        month = x.strftime("%b")
        month = "%" + month + "%"
        wherestr="where name like \'%s\' and date like \'%s\' ;"%(name,month)
    else:
        month = "%" + month + "%"
        wherestr="where name like \'%s\' and date like \'%s\' ;"%(name,month)
    sqlstr="SELECT * FROM blood_pressure %s"%wherestr
    p = cur.execute(sqlstr)
    registrants=cur.fetchall()
    cur.execute("select count(name)  from blood_pressure %s"%wherestr)
    count=str(cur.fetchone())
    count=count[1:-2]
    cur.execute("select avg(Systolic) from blood_pressure %s"%wherestr)
    avgsys=str(cur.fetchone())
    avgsys=avgsys[10:-7]
    cur.execute("select avg(Diastolic) from blood_pressure %s "%wherestr)
    avgdia=str(cur.fetchone())
    avgdia=avgdia[10:-7]
    cur.execute("select avg(Pulse) from blood_pressure %s "%wherestr)
    avgpul=str(cur.fetchone())
    avgpul=avgpul[10:-7]
    cur.close()
    conn.close()
    themonth=""
    if month == 'ALL':
        themonth="ALL"
    else:
        themonth=month[1:-1]

    return render_template("bpregistrants.html",themonth=themonth,registrants=registrants,name=name,count=count,avgsys=avgsys,avgdia=avgdia,avgpul=avgpul)
