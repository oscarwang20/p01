import urllib3
http = urllib3.PoolManager() # general requests manager that the rest of the functions will use.

def get_random_word(number: int = 1) -> str:
	r = http.request('GET', f'https://random-words-api.vercel.app/word?{number}')
	print(r)

get_random_word()
