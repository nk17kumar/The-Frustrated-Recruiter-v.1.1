from flask import Flask,render_template,jsonify
from bagroundVetting import *
from RecruiterBot import *
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)

Qno = {}
arr = ["Greeting Text","Why do you want to leave your previous job?","Why should we hire you?","Are you planning for higher education?","Okay! Nice talking to you. Bye :)"]
skillset = ["c++","java","python","database","communication","leadership"]

class store:
	bvc = {}
	scorecard = {}
	selected = {}
	ax = ""

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

@app.route('/analyse')
def analysis():
	html = "<html><head><title>Analysis</title></head><body>"
	html += "<table border = 10><tr><th>S.No.</th><th>Resume Name </th><th>C++</th><th>Java</th><th>Python</th><th>Database</th></tr>"
	sno = 1
	for key,v in store.scorecard.items():
		html+="<tr>"
		html+="<td>"+str(sno)+"</td>"
		html+="<td>"+str(key)+"</td>"
		html+="<td>"+str(store.scorecard[key]["c++"])+"</td>"
		html+="<td>"+str(store.scorecard[key]["java"])+"</td>"
		html+="<td>"+str(store.scorecard[key]["python"])+"</td>"
		html+="<td>"+str(store.scorecard[key]["database"])+"</td>"
		html+="</tr>"
		sno+=1
	html+="</table></body></html>"
	return html



@app.route('/chat/<txt>')
def chitchat(txt):
	id = getId(txt)
	txt = getTxt(txt)
	print "txt is : " + txt
	score = Chat.getSentimentScore(txt)
	qid = 0
	if Qno.has_key(id) == False:
		qid = 0
		store.bvc[id] = {}
	else:
		qid = Qno[id]
	store.bvc[id][qid] = score
	qid+=1
	d = {"txt":arr[qid]}
	Qno[id] = qid
	# if(id == 3):
	print "here is data : " + str(store.bvc)
	return jsonify(d);


@app.route('/eval' , methods = ['GET','POST'])
def bot():
	store.scorecard = Recruiter.eval()
	for key,v in store.scorecard.items():
		for skill in skillset:
			if skill in store.scorecard[key] == False:
				store.scorecard[key][skill] = 0
	chart()
	return jsonify(store.scorecard)
	# return scorecard

def autolabel(rects, xpos='center'):
	"""
	Attach a text label above each bar in *rects*, displaying its height.

	*xpos* indicates which side to place the text w.r.t. the center of
	the bar. It can be one of the following {'center', 'right', 'left'}.
	"""

	xpos = xpos.lower()  # normalize the case of the parameter
	ha = {'center': 'center', 'right': 'left', 'left': 'right'}
	offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

	for rect in rects:
		height = rect.get_height()
		store.ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
		'{}'.format(height), ha=ha[xpos], va='bottom')

# @app.route('/chart')
def chart():
	# populating resume names
	names = []
	std = []
	print "\n"
	print "Scorecard : " + str(store.scorecard)
	for k in store.scorecard.keys():
		names.append(k)
		std.append(0)

	score = {}

	# populating all skills
	for skill in skillset:
		tscore = []
		# print "\n" + "checking skill : " + str(skill)
		for key in store.scorecard.keys():
			# print "\n" + "rsume : " + str(key)
			tscore.append(store.scorecard[key][skill])
		score[skill] = tscore

	# print "\n"
	# print "names : " + str(names)
	# print "score : " + str(score)
	# men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
	# women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)

	# ind = np.arange(len(men_means))  # the x locations for the groups
	ind = np.arange(len(score["c++"]))
	width = 0.1  # the width of the bars

	fig, store.ax = plt.subplots()
	rect = {}

	# rects1 = store.ax.bar(ind - width/2, men_means, width, yerr=men_std,
	#                 color='SkyBlue', label='Men')
	# rects2 = store.ax.bar(ind + width/2, women_means, width, yerr=women_std,
	#                 color='IndianRed', label='Women')
	clr = ["SkyBlue","Green","Red","Orange","Yellow","Pink"]
	i=0
	for skill in skillset:
		i+=1
		i%=6
		rect[skill] = store.ax.bar(ind - i*width, score[skill], width, yerr=std,
		                color=clr[i], label=skill)

	# Add some text for labels, title and custom x-store.axis tick labels, etc.
	store.ax.set_ylabel('Scores')
	store.ax.set_title('Scores by skillset')
	store.ax.set_xticks(ind)
	# store.ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
	store.ax.set_xticklabels(names)
	store.ax.legend()


	# autolabel(rects1, "left")
	# autolabel(rects2, "right")

	for skill in skillset:
		autolabel(rect[skill],"left")

	# plt.show()
	plt.savefig("static/chart.png")


# chart()

if __name__ == "__main__":
	app.run(debug=True)
