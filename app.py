from flask import Flask, render_template, request, redirect, url_for
import dataset
import time
app = Flask(__name__)
db=dataset.connect("postgres://dnoofdvouckepf:77ac4f0e0b9601a4133128b3958be545820ee8dd02c0eefdd66f6629058d04ea@ec2-54-83-49-44.compute-1.amazonaws.com:5432/d31kebnsoenh20")


def reset_db():
	posts = db['posts']
	posts.drop()

#reset_db()
#print crash()


@app.route('/register' ,methods=["GET" , "POST"])
def registerpage():
	registerTable = db["register"]
	allr = list(registerTable.all())
	if request.method == 'GET':
		return render_template('register.html')
	else :
		form =request.form
		n_email=form["n_email"]
		f_name =form["f_name"]
		l_name=form["l_name"]
		us_name=form["us_name"]
		w_site=form["w_site"]

		entry = {"n_email":n_email , "f_name":f_name , "l_name":l_name , "us_name":us_name , "w_site":w_site }

		NameToCheck = us_name
		print len(list(registerTable.find(us_name=NameToCheck)))
		if len(list(registerTable.find(us_name=NameToCheck))) == 0:
			registerTable.insert(entry)
			allr = list(registerTable.all())
			return redirect('/feed')
		else:
			return redirect('/error')



@app.route('/feed', methods=["GET", "POST"])
def feedpage():
	registerTable = db["register"]
	postsTable = db["posts"]
	allposts = list(postsTable.all())[::-1]
	if request.method == 'GET':
		return render_template('feed.html', post=allposts)
	else :
		form =request.form
		post =form["post"]
		us_name=form["us_name"]
		time_string = time.strftime('%l:%M %p on %b %d, %Y')

		entry = {"post":post ,"us_name":us_name , "time":time_string}

		NameToCheck = us_name
		print len(list(registerTable.find(us_name=NameToCheck)))
		if len(list(registerTable.find(us_name=NameToCheck))) > 0:
			postsTable.insert(entry)
			allposts = list(postsTable.all())[::-1]
			return render_template('feed.html', post=allposts )
		else:
			return redirect('/register')


@app.route('/list')
def listpage():
	registerTable = db["register"]
	allcontacts = list (registerTable.all())[::-1]
	return render_template ("list.html" , contacts = allcontacts)
#..............................................#


@app.route('/')
@app.route('/home')
def homepage():
	return render_template("home.html")


@app.route('/error')
def errorpage():
	return render_template('error.html')

if __name__ == "__main__":
    app.run(port=3000)
