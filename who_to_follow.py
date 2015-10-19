from flask import Flask, url_for, render_template,request,json,jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from TwitterAPI import TwitterAPI
from keys import consumer_token,consumer_secret,access_token,access_secret

app = Flask(__name__)
api = TwitterAPI(consumer_token,consumer_secret,access_token,access_secret)

class Tweet():
	def __init__(self,username,verified,followers,tweets):
		self.username = username
		self.verified = bool(verified)
		self.followers = int(followers)
		self.tweets = int(tweets)


	def __repr__(self):
		return "username:%s,verfied:%s,followers:%d,tweets:%d"\
		%(self.username,self.verified,self.followers,self.tweets)


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
	list_of_tweets = map(lambda x:Tweet(x['screen_name'],x['verified'],\
		x['followers_count'],x['statuses_count']),dictOfStuff)
	only_verified = filter(lambda x: x.verified==True,list_of_tweets)
	sorted_by_followers = sorted(list_of_tweets,key=lambda tweet:tweet.followers)
	print(len(sorted_by_followers))
	if len(sorted_by_followers)>100:
		result = sorted_by_followers[9*(len(sorted_by_followers)/10):] #top decile
	elif len(sorted_by_followers)<10:
		result = sorted_by_followers
	else:
		result = sorted_by_followers[-10:]
	return str(map(lambda x:(x.username),result))




@app.route('/')
def index():
	return render_template("index.html")


@app.route('/results',methods=['POST'])
def backend():
	query = buildQuery(request.form['hashtags'])
	result = api.request('users/search',query).json()
	#return processResult(result)
	return render_template("results.html")
	





if __name__=='__main__':
	app.run(debug=True)