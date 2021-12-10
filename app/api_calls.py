import json
import urllib3
http = urllib3.PoolManager() # general requests manager that the rest of the functions will use.

def get_random_word(number: int = 1) -> list:
	'''Get a random word.

	Keyword arguments:
	number -- the number of expected returns (default 1)

	return a list of random words'''
	words = list()

	for i in range(number):
		r = http.request('GET', f'https://random-words-api.vercel.app/word') # request
		r = r.data # extracts text from http request
		r = json.loads(r) #turns json to dict.
		words.append(r[0]['word']) # extracts only the word data

	return words

print(get_random_word(2))
