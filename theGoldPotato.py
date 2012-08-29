import twitter
import MakeSentence
import datetime
import random
import math

#I understand this is hastily made and generally awful, but... it works. 
#The purpose of this bot is to show that Twitter is silly sometimes.
#I felt like I could tweet random sentences while mentioning trending topics 
#and follow people that hashtag 'followback' and you'll get loads of followers.

#That was my hypothesis. This is my experiment. 

datTweet = MakeSentence.RandomSentence() #Makes a random sentence using a module called MakeSentence that I found online
now = datetime.datetime.now() #get the current time
followNumber = int(math.floor(random.random()*10) + 1) #How many people are we going to follow this run through?
destroyNumber = int(math.floor(random.random()*5) + 1) #How many people should we unfollow this run through?

api = twitter.Api('VALIDATE WITH TWITTER')

hash_tag = api.GetTrendsDaily(exclude=None)[now.hour][0].name #We got find out what the top trend is so we can mention it
listOfPeopleToFollow = api.GetSearch(term='#teamfollowback', show_user='true', query_users=False) #get a list of people who will definitely follow us back
followerList = api.GetFollowers() #get a list of current followers
friendsList = api.GetFriends() #get a list of current friends


def main():	
	api.PostUpdate(datTweet + " " + hash_tag) #tweet a random sentence and mention the trending topic

	for i in range(followNumber): #follow some people
			api.CreateFriendship(listOfPeopleToFollow[i].user.screen_name) 
		
	if len(friendsList) - destroyNumber > 5: #unfollow some people
		for j in range(destroyNumber):
			api.DestroyFriendship(friendsList.pop().screen_name)
		
#where it all goes down
main()	
