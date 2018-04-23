from flask import Flask,render_template,jsonify
from bagroundVetting import *
from RecruiterBot import *

app = Flask(__name__)

bvc = {}
Qno = {}
arr = ["Greeting Text","Why do you want to leave your previous job?","Why should we hire you?","Are you planning for higher education?","Okay! Nice talking to you. Bye :)"]
scorecard = {}
def getId(txt):
	return txt.split('@')[0]

def getTxt(txt):
	s = txt.split('@')[1]
	ret = ""
	l = len(s)
	for i in range(0,l):
		if(s[i] == '%'):
			ret+=' '
		else:
			ret+=s[i]
	return ret

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/bvc')
def chatbox():
	return render_template("bvc.html")

@app.route('/chat/<txt>')
def chitchat(txt):
	id = getId(txt)
	txt = getTxt(txt)
	print "txt is : " + txt
	score = Chat.getSentimentScore(txt)
	qid = 0
	if Qno.has_key(id) == False:
		qid = 0
		bvc[id] = {}
	else:
		qid = Qno[id]
	bvc[id][qid] = score
	qid+=1
	d = {"txt":arr[qid]}
	Qno[id] = qid
	# if(id == 3):
	print "here is data : " + str(bvc)
	return jsonify(d);


@app.route('/eval' , methods = ['GET','POST'])
def bot():
	scorecard = Recruiter.eval()
	return jsonify(scorecard)


if __name__ == "__main__":
	app.run(debug=True)
