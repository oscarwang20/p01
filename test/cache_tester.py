#tests the caching
import sys
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+ "/app")
#imports from ../app/get_links.py
from app import get_links
from app.api_calls import get_random_word

print(get_links.get_definition("throw"))
print(get_links.get_synonyms("throw"))
print(get_links.get_wikipedia_links("throw"))

'''For caching check at most 100 api calls should be made.'''
for i in range(100):
	sleep(5)
	#gens random word
	word = get_random_word()
	print(word)
	#gets attributes that matter
	defn = get_links.get_definition(word)
	syn = get_links.get_synonyms(word)
	wiki = get_links.get_wikipedia_links(word)

	for j in range(10):
		if defn != get_links.get_definition(word):
			print("error in caching: defn")
			exit(1)
		elif syn != get_links.get_synonyms(word):
			print("error in caching: syns")
			exit(1)
		elif wiki != get_links.get_wikipedia_links(word):
			print("error in caching: wiki")
			exit(1)
