#tests the caching
import sys
import time
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+ "/app")

from app import get_links

word = "iceland"
print(get_links.get_an_edge(word))
print(get_links.generate_start_end())
