import twitter
import ConfigParser
import getopt
import os
import sys
import datetime
import random
import math
from bs4 import BeautifulSoup
import urllib

#This is a bot that tries to put a smile on da faces.
#It searches for people that are sharing quotes via twitter.
#It then tells the person that it likes their quote and 
#suggests a quote of its own. Then it follow the person
#for SUPER brownie points. 

api =  twitter.Api("VALIDATE WITH TWITTER HERE")

#Creates a list of people to bug from searching for people 
#hash tagging 'quotes'
listOfPeopleToBug = api.GetSearch(term='#quotes', show_user='true', query_users=False)

#Posts a retweet				  
def PostRetweet(id):
	url = 'http://api.twitter.com/1/statuses/retweet/%s.json' % id
	json = api._FetchUrl(url, post_data = {'dummy':None}) 

#fetches one of my quotes
def fetchShortQuote():
	quotes = ['Sanity and happiness are an impossible combination.',
		  'If you start wielding a hammer, then all your problems look like nails.',
		  "It's never too late to be who you might have been.",
		  "No one looks back on their life and remembers the nights they had plenty of sleep.",
		  "Everything should be as simple as it is, but not simpler.",
		  "When I'm sad, I stop being sad and be awesome instead.",
		  "There is nothing good or bad, but thinking makes it so.",
		  "If it won't bother you in a week, don't let it bother you today.",
		  "What you believe is what you become.",
		  "A ship is always safe at the shore - but that is not what it is built for.",
		##"If you start wielding a hammer, then all your problems look like nails. -Neil deGrass", <--- This is the max quote length
		  "If you're not confused, you're not paying attention.",
		  "A goal without a plan is just a wish.",
		  "Courage is fear that has said its prayers.",
		  "Everything's got a moral, if only you can find it.",
		  "Ambition is not a vice of little people.",
		  "Failure is success if we learn from it.",
		  "It's not what you look at that matters, it's what you see.",
		  "A clever man commits no minor blunders.",
		  "Great ideas often receive violent opposition from mediocre minds.",
		  "The dumbest people I know are those who know it all.",
		  "The truth is more important than the facts.",
		  "Love all, trust a few.",
		  "The gods too are fond of a joke.",
		  "It is dangerous to be sincere unless you are also stupid.",
		  "We need not think alike to love alike.",
		  "Middle age is youth without levity, and age without decay.",
		  "True friends stab you in the front.",
		  "A prudent question is one half of wisdom.",
		  "An ounce of emotion is equal to a ton of facts.",
		  "A witty saying proves nothing.",
		  "Creativity is the sudden cessation of stupidity.",
		  "Life is the flower for which love is the honey.",
		  "The truth is always exciting. Speak it, then. Life is dull without it.",
		  "Life is short, but there is always time enough for courtesy.",
		  "The purpose of life is a life of purpose.", 
		  "Our care should not be to have lived long as to have lived enough.",
		  "Life is just a chance to grow a soul.",
		  "Only a life lived for others is a life worthwhile.",
		  "How we spend our days is, of course, how we spend our lives.",
		  "Life is a succession of moments. To live each one is to succeed.",
		  "The goal of life is living in agreement with nature.",
		  "What you didn't see with your eyes, don't invent with your mouth.",
		  "Start with what is right rather than what is acceptable.",
		  "Nothing makes us as alone as our secrets.",
		  "The way we see the problem is the problem.",
		  "A candle loses nothing of its light by lighting another candle.",
		  "I don't know what the future holds, but I know who holds the future.",
		  "A generous man will prosper; he who refreshes others will himself be refreshed.",
		  "If the only prayer you said in your whole life was 'thank you', that would suffice.",
		  "If everyone is thinking alike, then somebody isn't thinking.",
		  "Visits always give pleasure, if not the arrival, the departure.",
		  "The fearful unbelief is the unbelief in yourself.",
		  "The past does equal the future.",
		  "In every failure lies the seeds of success.",
		  "Try not to become a man of success but a man of value.",
		  "Inspiration and genius--one in the same.",
		  "Every artist was first an amateur.",
		  "No great man ever complains of want of opportunities.",
		  "If you would create something, you must be something.",
		  "Experience is the child of thought, and thought is the child of action.",
		  "Men do less than they ought, unless they do all they can.",
		  "Let thy words be few.",
		  "The power of imagination makes us infinite."
		  "First say to yourself what you would be; and then do what you have to do.",
		  "You always miss 100% of the shots you don't take.",
		  "You only live once, but if you do it right, once is enough.",
		  "Never look down on someone, unless you're helping them up.",
		  "Being nice out of fear will never serve the purpose",
		  "If you're going to dream, dream big.",
		  "Choose a job you love and you will never have to work a day in your life.",
		  "Those who mind, shouldn't matter, and those who matter shouldn't mind.",
		  "If it doesn't fit, force it. If it breaks, it needed replacement anyway.",
		  "Life goes on.",
		  "Learn from yesterday, live for today, hope for tomorrow.",
		  "Never a failure, always a lesson.",
		  "Success is the greatest revenge.",
		  "If you want something you've never had, do something you've never done.",
		  "You weren't put on this Earth to be ordinary.",
		  "Pain is inevitable. Suffering is optional."] 
		  
	randInt = random.randint(0, len(quotes)-1)
	return quotes[randInt]

#Uses a random int to determine where it gets quotes
#0-5 scrape specific brainy quotes pages.
#6 uses one of my hard-coded in quotes	
def get_url():
	quote_type = random.randint(0,6)	
	
	if quote_type == 0:
		page_number = str(random.randint(1, 5))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/topics/topic_inspirational.html"
		else:
			url = "http://www.brainyquote.com/quotes/topics/topic_inspirational_"+page_number+".html"
	
	elif quote_type == 1:
		page_number = str(random.randint(1, 10))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/authors/a/albert_einstein.html"
		else:
			url = "http://www.brainyquote.com/quotes/authors/a/albert_einstein_"+page_number+".html"
			
	elif quote_type == 2:
		page_number = str(random.randint(1, 3))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/authors/b/buddha.html"
		else:
			url = "http://www.brainyquote.com/quotes/authors/b/buddha_"+page_number+".html"
			
	elif quote_type == 3:
		page_number = str(random.randint(1, 10))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/authors/m/mahatma_gandhi.html"
		else:
			url = "http://www.brainyquote.com/quotes/authors/m/mahatma_gandhi_"+page_number+".html"
			
	elif quote_type == 4:
		page_number = str(random.randint(1, 6))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/authors/s/steve_jobs.html"
		else:
			url = "http://www.brainyquote.com/quotes/authors/s/steve_jobs_"+page_number+".html"
			
	elif quote_type == 5:
		page_number = str(random.randint(1, 7))
		if page_number == "1":
			url = "http://www.brainyquote.com/quotes/authors/a/abraham_lincoln.html"
		else:
			url = "http://www.brainyquote.com/quotes/authors/a/abraham_lincoln_"+page_number+".html"
	
	elif quote_type == 6:
		url = None
				
	return url

#If the die in get_url() rolled a 6, this returns on of the hardcoded quotes
#Else, return a brainy quote. 	
def fetchQuote():	
	url = get_url()
	
	if url == None:
		return fetchShortQuote()
	else:
		quotes = []
		soup = BeautifulSoup(urllib.urlopen(url))
		tag = soup.find_all('span')
		string = "class=\"huge\""
		for i in tag:
			if str(i).find(string) != -1:
				quote = i.get_text()
				if len(quote) <= 87:
					quotes.append(quote)
					
		return quotes[random.randint(0, len(quotes)-1)]
	
#This puts all the pieces of the tweet together				  
def concat_tweet():
	at_mention = "@" + listOfPeopleToBug[0].user.screen_name
	fetchedQuote = False
	while (not fetchedQuote):
		quote = fetchQuote()
		if (quote != "We're sorry the page you're looking for can't be found."):
			full_tweet = at_mention + " I like your quote. Here's one of mine: \"" + fetchQuote() +"\""
			fetchedQuote = True
			
	return full_tweet

#My unfollow/follow algorithm to get/keep a steady amount of followers. 
def follow_unfollow():
	followerList = api.GetFollowers()
	friendsList = api.GetFriends()
	if 3*len(followerList) > len(friendsList):
		api.CreateFriendship(listOfPeopleToBug[0].user.screen_name)
		api.CreateFriendship(listOfPeopleToBug[1].user.screen_name)
	else:
		api.DestroyFriendship(friendsList.pop().screen_name)*4

#posts a tweet				  
def post_tweet():
	tweet = concat_tweet()
	api.PostUpdate(tweet)

def main():
	PostRetweet(listOfPeopleToBug[0].id)
	post_tweet()
	follow_unfollow()

##Run the Script
main()
	

		  

