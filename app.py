from flask import Flask, render_template, request, redirect, url_for
import dataset

app = Flask(__name__)
db=dataset.connect("postgres://dnoofdvouckepf:77ac4f0e0b9601a4133128b3958be545820ee8dd02c0eefdd66f6629058d04ea@ec2-54-83-49-44.compute-1.amazonaws.com:5432/d31kebnsoenh20")

@app.route('/')
@app.route('/register')
def registerpage():
	return render_template('register.html')

@app.route('/feed')
def feedpage():
	return render_template('feed.html')

@app.route('/home' , methods=["GET", "POST"])
def homepage():
	form =request.form
	n_email=form["n_email"]
	password=form["password"]
	f_name =form["f_name"]
	l_name=form["l_name"]
	us_name=form["us_name"]
	w_site=form["w_site"]

	registerTable = db["register"]
	entry = {"n_email":n_email ,"password":password , "f_name":f_name , "l_name":l_name , "us_name":us_name , "w_site":w_site }
	print list (registerTable.all())

	NameToCheck = us_name
	print len(list(registerTable.find(us_name=NameToCheck)))
	if len(list(registerTable.find(us_name=NameToCheck))) == 0:
		registerTable.insert(entry)
		return redirect('/list')
	else:
		return redirect('/error')



#..............................................#

@app.route('/list')
def listpage():
	registerTable = db["register"]
	allcontacts = list (registerTable.all())
	return render_template ("list.html" , contacts = allcontacts)


@app.route('/error')
def errorpage():
	return render_template('error.html')

if __name__ == "__main__":
    app.run(port=3000)
