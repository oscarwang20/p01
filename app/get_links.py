import api_calls

def get_definition(word: str) -> str:
	'''Returns the definition, if its cached, or retrieves and gets word definition from an api and caches it.

	Keyword arguments:
	word -- the word we want defined.

	Returns the definition of the word inputted.'''

	return api_calls.get_word_definition(word)

def get_synonyms(word: str) -> list:
	'''Returns the synonym of a word, if its cached, or retrieves and gets synonyms to a word from an api and caches it.

	Keyword argument:
	word -- the word we want the synonyms for.

	Returns a list of synonyms for the word inputted.'''

	return api_calls.get_word_synonyms(word)

def get_wikipedia_links(word: str) -> list:
	'''Returns the wikipedia links of a phrase, if its cached, and retrieves and gets the links from an api and caches it if not.

	Keyword argument:
	word -- the word or phrase we want the links for.

	Returns a list of links for the wikipedia page of the phrase inputted.'''

	return api_calls.get_wikipedia_links(word)
