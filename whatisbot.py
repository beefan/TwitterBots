import twitter
from bs4 import BeautifulSoup
import json
import sys 
import urllib
import random

#This twitter bot uses wolfram alpha to answer questions asked to it via mention
#or direct message. This is completely pointless for those who have smart phones
#But I created it because I had to use a dumbphone temporarily. 

#Define my global variables 
app_id = 'WOLFRAM-ALPHA-APP-ID'
api = twitter.Api('VALIDATE WITH TWITTER')

questions = []
answers = []

def get_dm_questions():
	
	direct_mentions = api.GetDirectMessages()
	contents = #the last question that was asked via direct message. 
			   #I originally did this using a .txt file, but I'm now
			   #using a google app engine database.
	
	for i in direct_mentions:
		if contents == i.text:
			direct_mentions = direct_mentions[:direct_mentions.index(i)]
			
	if len(direct_mentions) > 0:
	
		#Write the question asked to a database or file so we don't repeat questions
		#Using a google app engine db to do this now.
	
		for i in direct_mentions:
			questions.append([i.text, str(i.sender_screen_name), 'dm'])
			
		 
def follow_followers():
	friends = api.GetFriends()
	followers = api.GetFollowers()
	
	for i in followers:
		if i not in friends:
			try:
				api.CreateFriendship(i.screen_name)
			except:
				do = 'nothing'
	

def get_questions():
	'''Stores a 2D array of questions to be parsed and answered by whatisbot and the askers of the 
	   questions to the global variable, questions.
	   
	   Args: None
	   Returns: None '''
	
	mentions = api.GetMentions()
	contents = #the last question that was asked via mention. 
			   #I originally did this using a .txt file, but I'm now
			   #using a google app engine database.
			   
	for i in mentions:
		if contents == i.text:
			mentions = mentions[:mentions.index(i)]

	if len(mentions) > 0:
		
		#Write the question asked to a database or file so we don't repeat questions
		#Using a google app engine db to do this now.
		
		for i in mentions:
			if i.text[:10] == '@whatisbot':
				questions.append([i.text[11:], str(i.user.screen_name), 'pm'])

def get_random_fact():
	'''Parses json results from a mentalfloss script that generates random facts.
	
	   Args: None
	   Returns: random fact - string '''
	
	good = False
	while not good:
		url = "http://mentalfloss.com/amazingfactgenerator/load-fact.php"
		data = json.load(urllib.urlopen(url))
		return_this =  data["post_content"].encode('ascii','ignore')
		
		if '<' in return_this and '>' in return_this:
			sub = return_this[return_this.index('<'):return_this.index('>')]
			return_this.replace(sub, "");
			
		if len(str(return_this)) < 125:
			good = True
	
	return str(return_this)
	

def answer_question(question):
	'''Appends an answer to a passed in question to the global array, answers. Also stores the asker 
	   of the question to said array.
	
	   Args: question - [a question to be answered, the asker of the question]
	   Returns: None '''
	
	_question = question[0]
	asker = question[1]
	dm_or_pm = question[2]
	
	url = "http://api.wolframalpha.com/v2/query?input="+_question+"&appid="+app_id
	soup = BeautifulSoup(urllib.urlopen(url))
	tag = soup.find_all('plaintext')
	
	if len(tag) > 2:
		answer = str(tag[1].get_text().encode('ascii','ignore'))
		if len(answer) < 120:
			answers.append([asker, " " + answer, dm_or_pm])
		else:
			pointer = 120
			iterate = True
			answers.append([asker," " + answer[:120] + "...", dm_or_pm])
			while (iterate):
				if ((pointer + 120) < len(answer)):
					pointer = pointer + 120
					answers.append([asker, " " + answer[121:pointer] + "...", dm_or_pm])
				else:
					answers.append([asker, " " + answer[121:], dm_or_pm])
					iterate = False
	
			
	else:
		if len(_question) <= 60:
			answers.append([asker, " I'm sorry. I couldn't find an answer to your question, '"+_question+"'." , dm_or_pm])
		else:
			answers.append([asker, " I'm sorry. I couldn't find an answer to your question, '"+_question[:60]+"'..." , dm_or_pm])
		

def tweet_answers():
	'''Tweets all of the answers to the questions asked.
	   
	   Args: None
	   Returns: None'''
	
	for i in answers:
		if i[2] == 'pm':
			api.PostUpdate("@"+i[0]+i[1])
		elif i[2] == 'dm':
			api.PostDirectMessage(i[0], i[1])



def main():	
	
	tweet_fact = random.randint(0,1300)
	follow_followers()
	get_dm_questions()
	get_questions()
	e2.put()
	
	if len(questions) > 0:
		for i in questions:
			print i
			answer_question(i)
	print questions
	print answers
	tweet_answers()
	
	if tweet_fact == 13:
		api.PostUpdate(get_random_fact() + " #NowYouKnow")
		
main()
