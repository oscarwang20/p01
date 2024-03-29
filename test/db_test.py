import sys
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+ "/app")

from db_builder import *

def show_user_exists(username):
    if check_user_exists(username):
        print(username + " exists")
    else:
        print(username + " does not exist")

def show_password_matches(username, password):
    if check_password_matches(username, password):
        print("correct password for " + username)
    else:
        print("incorrect password for " + username)

if __name__ == "__main__":
    dbsetup()
    show_user_exists("bob")
    show_user_exists("joe")
    insert_user("bob", "good password")
    insert_user("joe", "hi dere")
    show_user_exists("bob")
    show_user_exists("joe")
    show_password_matches("bob", "bad password")
    show_password_matches("bob", "good password")
    show_password_matches("joe", "hi dere")
    show_password_matches("joe", "bye dere")
