
#schéma des exeptions possibles 

try:
    fichier = open("article.md")
except FileNotFoundError:
    print("The file does not exists")

#quand la valeur n'est pas la bonne 
try:
    age = int("Hello")
except ValueError:
    print("Value must be a number")


#ask the user to choose a filename in article 
#and then print its content 
#if the file does not exist, ask the user again
#using try and except 

from pathlib import Path

articles_dir = Path("../articles")

while True:

    try:
        file_name = input("Enter the name of the article: \n ")
        file = open(file_name, "r")
        print(file.read())
        file.close()
        break

    except FileNotFoundError:
        print("The file does not exist")

# ask user to enter the name of the file
#try to read the content of the .md file
#print the name if the file exists, else ask again

def show_article():
    ask_again = True 
    content = ""
    while ask_again :
        fname = input("enter article's name :")
        file_path = Path("../../../1_blog/article")/ (fname + ".md")
        try : 
            content = file_path.read_text()
        except FileNotFoundError : 
            print("invalid filename")
        else : 
            ask_again = False
    print (content)


#rajouter supp commentaire 
#pas de comm vide 
#bien type/ commente et documente 
#main = route pour les commentaires app.get app.post 