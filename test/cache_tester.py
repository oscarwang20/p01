#tests the caching
import sys
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#imports from ../app/get_links.py
from app.get_links import Cache_manager
