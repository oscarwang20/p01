import codecs
import json
import urllib3
http = urllib3.PoolManager() # general requests manager that the rest of the functions will use.
keys = {
	"webster_dictionary": open("keys/MerriamWebster/Dictionary.key", "r").read().rstrip(),
	"webster_thesaurus": open("keys/MerriamWebster/Thesaurus.key", "r").read().rstrip(),
}

def get_random_word(number: int = 1) -> list:
	'''Get a random word.

	Keyword arguments:
	number -- the number of expected returns (default 1)

	return a list of random words'''
	words = list()

	for i in range(number):
		r = http.request('GET', f'https://random-words-api.vercel.app/word') # request
		r = r.data #data from request
		r = json.loads(r) #loads data into json
		words.append(r[0]['word']) # extracts only the word data

	return words

def get_word_dictionary_raw(word: str) -> dict:
	'''Gets the definition and metadata of a word.

	Keyword arguments:
	word -- the word you want a definition of

	return a doc of the word's attributes.'''
	global keys

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
	raw = raw[0] #extracts the most common definition of the word
	raw = raw['shortdef'] #gets the quick definitions

	return raw[0] #gets the most popular short defintion

def get_word_thesaurus_raw(word: str) -> dict:
	'''Gets MerriamWebster's raw synonyms archive for a word.

	Keyword arguments:
	word -- the word you want synonymized

	returns the attributes of the api response for that word'''
	global keys

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

	if raw[0]['meta']['id'] != word: #if the first result (a.k.a closest fit) isn't the word itself, there are no synonyms so we can trash the dataset
		return []
	else:
		return raw[0]['meta']['syns'][0] #returns synonyms for most likely definition.

##print(get_random_word(2))
##print(get_word_definition('apple'))
print(get_word_synonyms('apple'))
