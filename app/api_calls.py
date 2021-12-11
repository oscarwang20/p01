import json
import urllib3
http = urllib3.PoolManager() # general requests manager that the rest of the functions will use.
keys = {
	"webster_dictionary": open("keys/MerriamWebster/Dictionary.key", "r").read()
}

def get_random_word(number: int = 1) -> list:
	'''Get a random word.

	Keyword arguments:
	number -- the number of expected returns (default 1)

	return a list of random words'''
	words = list()

	for i in range(number):
		r = http.request('GET', f'https://random-words-api.vercel.app/word') # request
		r = r.data.decode('utf8') #data from request
		r = json.loads(r) #loads data into json
		words.append(r[0]['word']) # extracts only the word data

	return words

def get_word_definition(word: str) -> dict:
	'''Gets the definition and synonyms of a word.

	Keyword arguments:
	word -- the word you want a definition of

	return a doc of the word's attributes.'''
	global keys

	r = http.request('GET', f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={keys["webster_dictionary"]}') # requests word from dictionary api with provisioned key

	r = r.data.decode('utf-8') #gets json from response
	r = json.loads(r)
	return r

print(get_random_word(2))
print(get_word_definition("apple"))