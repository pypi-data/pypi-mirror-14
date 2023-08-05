import abc
import operator
from ..tools.tweet_parser import TweetParser

class BaseCollection(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		pass

	'''
		returns a list of test values for all 
		tweets, should return a dictionary
	'''
	def get_texts(self):
		return [tweet[text] for tweet in self]

	'''
		returns a dictionary with
		counts for the number of 
		top entities requested
	'''
	def top_entities(self, requested_entities):
		returndict = {}
		returnstructure = {}
		tweet_parser = TweetParser()
		#init dempty dict for all entity types
		for entity_type in requested_entities:
			returndict[entity_type] = {}

		for tweet in self.get_iterator():
			for entity_type in requested_entities:
				for entity in tweet_parser.get_entity(entity_type, tweet):
					if entity_type == 'user_mentions':
						entity_value = tweet_parser.get_entity_field('id_str', entity)
					elif entity_type == 'hashtags' or entity_type == 'symbols':
						entity_value = tweet_parser.get_entity_field('text', entity)
					else:
						entity_value = tweet_parser.get_entity_field('url', entity)

					if entity_value in returndict[entity_type]:
						returndict[entity_type][entity_value] += 1
					else:
						returndict[entity_type][entity_value] = 1

		for entity_type in returndict:
			if len(returndict[entity_type]) < 1:
				returnstructure[entity_type] = {}
			else:
				sorted_list = sorted(returndict[entity_type].items(), key=operator.itemgetter(1), reverse=True)
				# if the user put in 0 return all entites
				# otherwise slice the array and return the
				# number of top things they asked for
				# if the list is too short throw in None
				if requested_entities[entity_type] == 0:
					returnstructure[entity_type] = {name: count for name, count in sorted_list}
				elif len(sorted_list) < requested_entities[entity_type]:
					returnstructure[entity_type] = {name: count for name, count in sorted_list}
					for i in range(0,requested_entities[entity_type]-len(sorted_list)):
						returnstructure[entity_type][i] = None
				else:
					returnstructure[entity_type] = {name: count for name, count in sorted_list[0:requested_entities[entity_type]]}
		return returnstructure
