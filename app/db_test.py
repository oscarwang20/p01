from db_builder import *

def show_user_exists(username):
    if check_user_exists(username):
        print(username + " exists")
    else:
        print(username + " does not exist")

if __name__ == "__main__":
    dbsetup()
    show_user_exists("bob")
    show_user_exists("joe")
    insert_user("bob", "good password")
    show_user_exists("bob")
    show_user_exists("joe")
