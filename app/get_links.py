import api_calls
from cache import Cache_manager
cache = Cache_manager()

def cache_on_command(word:str) -> None:
	'''Caches a word if its not already cached.'''
	if not cache.is_cached(word):
		cache.insert_word(word)

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

	return api_calls.get_wikipedia_links(word)
