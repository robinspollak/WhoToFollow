from flask import Flask, url_for, render_template,redirect,request,json,jsonify
from TwitterAPI import TwitterAPI
from keys import * #for local development
import os

app = Flask(__name__)
#api = TwitterAPI(os.environ['CONSUMER_TOKEN'],os.environ['CONSUMER_SECRET'],\
#os.environ['ACCESS_TOKEN'],os.environ['ACCESS_SECRET']) #heroku environment vars
api = TwitterAPI(consumer_token,consumer_secret,access_token,access_secret) #for local development

class User():
  """
  a class for reading in users from the JSON returned by
  Twitter's search API. Allows for sorting, and easy
  access to data for relevant list comprehension
  """
  def __init__(self,username,name,verified,followers,tweets,profpic_url):
    self.username = username
    self.name=name
    self.verified = bool(verified)
    self.followers = int(followers)
    self.tweets = int(tweets)
    self.profpic_url = profpic_url

  def __repr__(self): # for debugging
    return "username:%s,name:%sverfied:%s,followers:%d,tweets:%d,profpic_url:%s"\
    %(self.username,self.name,self.verified,self.followers,self.tweets,self.profpic_url)

def buildQuery(all_keywords):
  """
  given a long string of keywords, returns a formatted query
  that will then be passed to the Twitter API
  """
  first = True
  query_string = ''
  for string in all_keywords.split(" "):
    if first:
      first = False
      query_string+=string
    else:
      query_string+='+%s'%(string)
  return {'q':query_string,'count':500} # 500 users that fit the keyword combination

def processResult(dict_of_results):
  """
  reads in the list of results into the User class and then
  sorts by verification, and number of followers and returns
  some result based on number of suitable results
  """
  list_of_users = map(lambda x:User(x['screen_name'],x['name'],x['verified'],\
    x['followers_count'],x['statuses_count'],x['profile_image_url']),dict_of_results)
  only_verified = filter(lambda x: x.verified==True,list_of_users)
  sorted_by_followers = sorted(list_of_users,key=lambda tweet:tweet.followers)
  if len(sorted_by_followers)>100: 
    result = sorted_by_followers[9*(len(sorted_by_followers)/10):] #top decile
  elif len(sorted_by_followers)<10:
    result = sorted_by_followers # all results, there are less than 10
  else:
    result = sorted_by_followers[-10:] # return top 10 results
  return render_template('results.html',result=result[::-1]) # put the list in descending order

def valid(query): 
  """ Makes sure the query isn't empty. """
  return query.replace(" ","") != "" and query is not None

@app.route('/') #home page
def index():
  return render_template('index.html')

@app.route('/results', methods=['POST'])
def submit():
  """
  If the user submits a form with a valid topic, we redirect to that topic's
  page. If they submit an empty POST, we redirect back to the index page.
  """
  if valid(request.form['hashtags']):
    return redirect('/' + request.form['hashtags'])
  else:
    return redirect('/')

@app.route('/<topic>',methods=['GET']) #results page
def backend(topic):
  assert valid(topic) # this route shouldn't even trigger if topic is empty
  query = buildQuery(topic)
  result = api.request('users/search', query).json()
  return processResult(result)
  
if __name__=='__main__':
  app.run(debug=True)
