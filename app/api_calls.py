import json
import os
import urllib3
http = urllib3.PoolManager() # general requests manager that the rest of the functions will use.
#makes it work when importing from a different dir
abs_path = os.path.dirname(__file__)
keys = {
	"webster_dictionary": open(abs_path + "/keys/MerriamWebster/Dictionary.key", "r").read().rstrip(),
	"webster_thesaurus": open(abs_path + "/keys/MerriamWebster/Thesaurus.key", "r").read().rstrip(),
}

#DEBUG stuff
DEBUG = False
def key_used(api:str, debug:bool = DEBUG):
	if debug:
		print(f"{api} was invoked")

def debug(msg:str, debug:bool = DEBUG):
	if debug:
		print(msg)

def is_word_frequent(word: str) -> bool:
	fr = http.request('GET', f'https://api.datamuse.com/words?sp={word}&md=f&max=1')
	fr = fr.data
	fr = json.loads(fr)

	return fr and (fr[0]['score'] > 100000) # must appear at least 100k times per million words

def get_word() -> str:
	r = http.request('GET', f'https://random-words-api.vercel.app/word') # request
	r = r.data #data from request
	r = json.loads(r) #loads data into json
	return r[0]['word'] # extracts only the word data

def get_random_words(number: int = 1) -> list:
	'''Get a random word list.

	Keyword arguments:
	number -- the number of expected returns (default 1)

	return a list of random words'''
	words = list()

	for i in range(number):
		w = get_word()
		is_freq = is_word_frequent(w)
		while not is_freq:
			# print(w)
			w = get_word()
			is_freq = is_word_frequent(w)
		words.append(w)

	return words

def get_random_word() -> str:
	'''Gets exactly 1 random word'''
	return get_random_words()[0]

def get_word_dictionary_raw(word: str) -> dict:
	'''Gets the definition and metadata of a word.

	Keyword arguments:
	word -- the word you want a definition of

	return a doc of the word's attributes.'''
	global keys
	key_used("dictionary")

	word = word.lower()
	r = http.request('GET', f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={keys["webster_dictionary"]}') # requests word from dictionary api with provisioned key

	r = r.data #gets json from response
	r = json.loads(r) #loads json

	return r

def get_word_definition(word: str) -> str:
	'''Gets the definition of a word.

	Keyword arguments:
	word -- the word you want defined

	returns the string that's its definition'''

	raw = get_word_dictionary_raw(word)
	if len(raw) == 0 or isinstance(raw[0], str):#checks if it returned no data OR suggestions for words (aka it has no data)
		wiki_desc = get_wikipedia_desc(word)
		if wiki_desc == None: #if a wikipedia description exists return that, if not don't.
			return 'There is no definition available.'
		else:
			return wiki_desc
	else:
		raw = raw[0] #extracts the most common definition of the word
		raw = raw['shortdef'] #gets the quick definitions

		return raw[0] #gets the most popular short definition

def get_word_thesaurus_raw(word: str) -> dict:
	'''Gets MerriamWebster's raw synonyms archive for a word.

	Keyword arguments:
	word -- the word you want synonymized

	returns the attributes of the api response for that word'''
	global keys
	key_used("thesaurus")

	r = http.request('GET', f'https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={keys["webster_thesaurus"]}')

	r = r.data #gets data from request
	r = json.loads(r)

	return r

def get_word_synonyms(word: str) -> list:
	'''Gets synonyms for the word.

	Keyword arguments:
	word -- the word you want synonymized

	returns the attributes of the api response for that word, none if there's not an exact match'''

	raw = get_word_thesaurus_raw(word)

	if len(raw) == 0 or isinstance(raw[0], str):#checks if it returned no data OR suggestions for close words (aka it has no data)
		return []
	elif raw[0]['meta']['id'].lower() != word.lower(): #if the first result (a.k.a closest fit) isn't the word itself, there are no synonyms so we can trash the dataset (this is different from the above as words can be part of sayings that have synonyms but not have synonyms themselves)
		return []
	else:
		return raw[0]['meta']['syns'][0] #returns synonyms for most likely definition.

def get_wikipedia_desc(query:str) -> str:
	'''Gets the wikipedia description for a query

	Keyword arguments:
	query -- the current page we're on in the game

	Retursn the description wikipedia has for that page'''
	query = query.replace(' ', '%20') #gets appropriate url codes for api query
	url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&titles={query}&prop=description'

	r = http.request('GET', url)
	r = r.data
	r = json.loads(r)
	r = r['query']
	r = r['pages']

	if '-1' in r.keys(): #no pages found
		return None
	else:
		r = r[list(r.keys())[0]]#extracts the most relevant page
		if 'description' not in r.keys(): #if it has no description return none
			return None
		else:
			return r['description']

def get_wikipedia_links(query: str, links:int = 'max') -> list:
	'''Gets wikipedia links to a word.

	Keyword arguments:
	query -- the current page we're on in the game
	links -- the number of links you want in your query

	returns all wikipedia links for that specific word and page'''
	key_used("wikipedia")

	link_list = []

	debug(query)
	query = query.replace(' ', '%20') #replaces spaces in query with appropriate url codes
	url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&titles={query}&prop=links&pllimit={links}'

	while url is not '':
		r = http.request('GET', url)#gets api response
		r = r.data#extracts data
		r = json.loads(r)#loads the json
		if 'batchcomplete' not in r.keys(): #gets the next page pointer if it exists
			url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&titles={query}&prop=links&pllimit={links}&plcontinue={r["continue"]["plcontinue"]}'
		else:
			url = ''
		r = r['query']#extracts main chunk of data from json
		r = r['pages']#extracts pages concerning this topic

		if '-1' in r.keys(): #checks for the no page error return. If its present, return nothing as we don't have a page on it.
			return link_list
		else:
			r = r[list(r.keys())[0]]#extracts the most relevant page's links
			if links in r.keys():
				r = r['links']#extracts links in the page

				for link in r:#extracts title data from the api
					link_list.append(link['title'])


	debug(len(link_list))
	return link_list
##print(get_random_word(2))
##print(get_word_definition('sdadasd'))
##print(get_word_synonyms('sdadasd'))
##print(get_wikipedia_links("i"))
