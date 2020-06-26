from flask import Flask,render_template,request,redirect,flash,send_file,make_response,Response
import pandas as pd
from werkzeug.utils import secure_filename
import csv
import time 
import jsonify
import json
import pandas as pd
import io
from csv import reader
from bs4 import BeautifulSoup
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
import pandas as pd
import requests
from tqdm.notebook import tqdm
import csv
from nltk import word_tokenize
from spellchecker import SpellChecker
spell = SpellChecker()
import os
from flask import Flask, session
from flask_session import Session
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'}

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#print(pd.read_html('https://iul.ac.in/admissioninfo/FeeInd.aspx'))
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('Auto.html')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/tables',methods=['GET','POST'])
def tables():
	return data.da.to_html()

@app.route('/corr',methods=['GET','POST'])
def corr():
	return data.da.corr().to_html()

@app.route('/data',methods=['GET','POST'])
def data():
	if request.method=='POST':
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			data.da=pd.read_csv(file)
			col=data.da.columns
			return render_template('Auto.html',data1=data.da.to_html(),data2=col)
	else:
		return render_template('Auto.html',data1=data.da.to_html(),data2=data.da.columns)


@app.route('/datatypes',methods=['GET','POST'])
def datatypes():
	listr={}
	for i,j in zip(data.da.columns,pd.DataFrame(data.da.dtypes)[0]):
		listr[i]=str(j)
	return pd.DataFrame.from_dict(listr,orient='index').to_html()


@app.route('/columns',methods=['GET','POST'])
def testing():
	col=data.da.columns
	col=pd.DataFrame(col)
	return col.to_html()



@app.route('/shape',methods=['GET','POST'])
def shape():
	x=data.da.shape
	s="<h1>"+str(x[0])+" Rows & "+str(x[1])+" Columns"+"</h1>"
	return s


@app.route('/colvalues',methods=['POST'])
def colvalues():
	f=request.get_json(force=True)
	print(f)
	print("Got or not")
	s=data.da[f]
	return s.to_html()

@app.route('/unique',methods=['POST'])
def unique():
	f=request.get_json(force=True)
	s=pd.DataFrame(data.da[f[0]].unique().tolist(),columns=[f])
	return s.to_html()

@app.route('/nunique',methods=['GET','POST'])
def nunique():
	f=request.get_json(force=True)
	print(f)
	s="<h1>"+"Number of Unique Values are "+str(data.da[f[0]].nunique())+" in "+str(f[0])+" column"+"</h1>"
	return s

@app.route('/vcounts',methods=['POST','GET'])
def vcounts():
	f=request.get_json(force=True)
	s=pd.DataFrame(data.da[f[0]].value_counts()).reset_index() 
	return s.to_html()

@app.route('/nulls',methods=['POST','GET'])
def nulls():
	f=request.get_json(force=True)
	print("Received data is ",f)
	s="<h1>"+"Total null values in this column are "+str(data.da[f[0]].isnull().sum())+"</h1>" 
	return s



@app.route('/describe',methods=['POST','GET'])
def describe():
	f=request.get_json(force=True)
	s=pd.DataFrame(data.da[f[0]].describe())
	return s.to_html()

@app.route('/progress',methods=['POST','GET'])
def progress():
	#print("Progress Received")
	return "Hwee"

@app.route('/typo',methods=['POST','GET'])
def typo():
	f=request.get_json(force=True)
	#print("Received==",f)
	#s=pd.DataFrame(data.da[f[0]].describe())
	categorical=[]
	correct={}
	for c,j in enumerate(data.da[f[0]]):
		l=[]
		print(c)
		try:
			l=word_tokenize(j)
		except:
			pass
		if len(l)>=0:
			for word in l:
				try:
					corrected=spell.correction(word)
					if corrected!=word:
						correct[word]=corrected
				except:
					pass
	if correct:
		return pd.DataFrame.from_dict(correct,orient='index').to_html()
	return "<h1> No typo found </h1>"



@app.route('/dash',methods=['POST','GET'])
def dash():
	listr={}
	for i,j in zip(data.da.columns,pd.DataFrame(data.da.dtypes)[0]):
		listr[i]=str(j)
	return render_template('Dashboard.html',listr=listr)


@app.route('/Bar',methods=['POST','GET'])
def Bar():
	if request.method == 'POST':
		Bar.f=request.get_json(force=True)
		print("Received")

	try:
		print(Bar.f,"present")
		import io
		import base64
		from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
		import matplotlib.pyplot as plt
		import seaborn as sns
		import jinja2
		import numpy as np
		fig,ax=plt.subplots(figsize=(6,6))
		ax=sns.set(style="darkgrid")
		if len(Bar.f)==3:
			if Bar.f[2]=="Line":
				sns.lineplot(data.da[Bar.f[0]],data.da[Bar.f[1]])
			elif Bar.f[2]=="Bar":
				sns.barplot(data.da[Bar.f[0]],data.da[Bar.f[1]])
			elif Bar.f[2]=="Scatter":
				sns.scatterplot(data.da[Bar.f[0]],data.da[Bar.f[1]])
			else:
				sns.barplot(data.da[Bar.f[0]],data.da[Bar.f[1]])
		elif len(Bar.f)==2:
			if Bar.f[1]=="Count":
				sns.countplot(data.da[Bar.f[0]])
			elif Bar.f[1]=="Dist":
				sns.distplot(data.da[Bar.f[0]])
			elif Bar.f[1]=="Pie":
				print("Value received as",Bar.f[0])
				x=data.da[Bar.f[0]].value_counts().to_dict()
				print("XXX",x)
				slicer=list(x.values())
				labels=list(x.keys())
				print(slicer,labels)
				plt.pie(slicer,explode=None ,labels=labels,startangle = 90,autopct='%1.0f%%', shadow = True)

		else:
			sns.heatmap(data.da.select_dtypes(exclude=['object']))
		
		canvas=FigureCanvas(fig)
		img = io.BytesIO()
		fig.savefig(img)
		img.seek(0)
		return send_file(img,mimetype='img/png')
	except:
		return("Please Select appropiate coluns and visualization strategy")

@app.route('/scraper',methods=['POST','GET'])
def scraper():
	try:
		return render_template('Scraper.html',data=data.da)
	except:
		return render_template('Scraper.html')


@app.route('/scraped',methods=['POST','GET'])
def scraped():
	try:
		url=request.get_json(force=True)
		print(url)
		#try:
		res=requests.get(url)
		soup=BeautifulSoup(res.text,'html.parser')
		tdr=[]
		tdd=[]
		dic={}
		for c,i in enumerate(soup.find_all('tr')):
			tdd=[]
			for td in i.find_all('td'):
				tdd.append(td.text.strip())
			dic[c]=tdd
		scraped.df=pd.DataFrame.from_dict(dic, orient='index')
		return scraped.df.to_html()
	except:
		return "You did something Wrong or table isn't present"

@app.route('/download1',methods=['POST','GET'])
def download1():
	x=request.args.get('idd')
	print(x)
	#scraped.df.to_csv('file.csv')
	#print(scraped.df)
	resp = make_response(data.da.to_csv(index=False))
	resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
	resp.headers["Content-Type"] = "text/csv"
	return resp


@app.route('/profiled',methods=['POST','GET'])
def profiled():
	try:
		from pandas_profiling import ProfileReport
		df = ProfileReport(data.da)
		df=df.to_file(r"templates/your_report.html")
		return render_template('your_report.html')
	except:
		return "Return to first page and upload the CSV"


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess=Session()
    sess.init_app(app)

    app.debug = True
    app.run()