import api_calls
import random
from cache import Cache_manager
cache = Cache_manager()

def cache_on_command(word:str) -> None:
	'''Caches a word if its not already cached.'''
	if not cache.is_cached(word):
		cache.insert_word(word)

def get_random_words(num:int) -> list:
	return api_calls.get_random_words(num)

def get_random_word() -> str:
	return api_calls.get_random_word()

def get_definition(word: str) -> str:
	'''Returns the definition, if its cached, or retrieves and gets word definition from an api and caches it.

	Keyword arguments:
	word -- the word we want defined.

	Returns the definition of the word inputted.'''
	#caches word if it wasn't already cached
	cache_on_command(word)

	return cache.define(word)

def get_synonyms(word: str) -> list:
	'''Returns the synonym of a word, if its cached, or retrieves and gets synonyms to a word from an api and caches it.

	Keyword argument:
	word -- the word we want the synonyms for.

	Returns a list of synonyms for the word inputted.'''
	cache_on_command(word)

	return cache.synonyms(word)

def get_wikipedia_links(word: str) -> list:
	'''Returns the wikipedia links of a phrase, if its cached, and retrieves and gets the links from an api and caches it if not.

	Keyword argument:
	word -- the word or phrase we want the links for.

	Returns a list of links for the wikipedia page of the phrase inputted.'''
	cache_on_command(word)

	return cache.wikipedia_links(word)

def get_an_edge(word: str, burned_edges: list = []) -> str:
	'''Gets a (graph theory) edge from one word to the next.

	Keyword argument:
	word -- the word we're starting on.

	Returns a link to the next word'''
	all_links = get_synonyms(word) + get_wikipedia_links(word)

	for item in burned_edges:
		while item in all_links:#removes burned edges from choice
			all_links.remove(item)

	if len(all_links) == 0: #if list empty, no nodes, return empty
		return None

	item = random.choice(all_links)
	return item

def get_end_word(word: str, jumps:int = 7) -> str:
	'''Gets a target word that is reachable from the original word.

	Keyword argument:
	word -- starting word
	jumps -- max number of jumps between the two

	Returns target word'''
	path = [word] #word is the first in the path
	path_burned_forks = {word: list()} #bad links for a given path
	while len(path) < (jumps + 1):
		word = path[-1]
		path.append(get_an_edge(word,path_burned_forks[word]))

		if path[-1] == None: #where there's no available link from second to last to current word
			if len(path) < 3: #if there's not enough elements to remove None + the last word and have a word remaining
				return None #there's no valid end word
			else:
				path = path[0:-1] # cuts off last element, None
				path_burned_forks[path[-2]].append(path.pop(-1)) # burned path for second to last element is the last element as that has no connections
		else:
			path_burned_forks[path[-1]] = list() #creates new list of burned paths for valid words

	return path[-1]
def generate_start_end() -> tuple:
	'''returns a tuple with a start and end word pair'''
	start = None
	end = None
	while start is None or end is None:
		start = get_random_word()
		end = get_end_word(start)
	return (start, end)
