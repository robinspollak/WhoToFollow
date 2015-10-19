from flask import Flask, url_for, render_template,redirect,request,json,jsonify,url_for
from TwitterAPI import TwitterAPI
#from keys import * #for local development
import os

app = Flask(__name__)
api = TwitterAPI(os.environ['CONSUMER_TOKEN'],os.environ['CONSUMER_SECRET'],\
os.environ['ACCESS_TOKEN'],os.environ['ACCESS_SECRET']) #heroku environment vars
#api = TwitterAPI(consumer_token,consumer_secret,access_token,access_secret) #for local development

class Tweet():
	def __init__(self,username,name,verified,followers,tweets,profpic_url):
		self.username = username
		self.name=name
		self.verified = bool(verified)
		self.followers = int(followers)
		self.tweets = int(tweets)
		self.profpic_url = profpic_url


	def __repr__(self):
		return "username:%s,name:%sverfied:%s,followers:%d,tweets:%d,profpic_url:%s"\
		%(self.username,self.name,self.verified,self.followers,self.tweets,self.profpic_url)


def buildQuery(listOfStrings):
	first = True
	query_string = ''
	for string in listOfStrings.split(" "):
		if first:
			first = False
			query_string+=string
		else:
			query_string+='+%s'%(string)
	return {'q':query_string,'count':500}

def processResult(dictOfStuff):
	list_of_tweets = map(lambda x:Tweet(x['screen_name'],x['name'],x['verified'],\
		x['followers_count'],x['statuses_count'],x['profile_image_url']),dictOfStuff)
	only_verified = filter(lambda x: x.verified==True,list_of_tweets)
	sorted_by_followers = sorted(list_of_tweets,key=lambda tweet:tweet.followers)
	if len(sorted_by_followers)>100:
		result = sorted_by_followers[9*(len(sorted_by_followers)/10):] #top decile
	elif len(sorted_by_followers)<10:
		result = sorted_by_followers
	else:
		result = sorted_by_followers[-10:]
	return render_template('results.html',result=result[::-1])

def valid(query):
	if (query.replace(" ","")!=""):
		return True
	return False

def handleData(data):
	if valid(data):
		query = buildQuery(request.form['hashtags'])
		result = api.request('users/search',query).json()
		return processResult(result)
	else:
		return redirect(url_for('index'))





@app.route('/')
def index():
	return render_template("index.html")


@app.route('/results',methods=['POST'])
def backend():
	return handleData(request.form['hashtags'])
	

	





if __name__=='__main__':
	app.run(debug=True)