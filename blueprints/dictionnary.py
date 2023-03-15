from flask import Blueprint, request, jsonify, render_template
from model.db_words import Dict
from markupsafe import escape
import json

dict = Blueprint('dictionnary', __name__)
router = "/api/words/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = Dict(connect['host'],connect['user'],connect['password'],connect['database'])

@dict.route(f"{router}get/<int:id>",methods=['GET'])
def getWord(id):
    if request.method == "GET":
        return jsonify(db.getWord(id))

@dict.route(f"{router}add", methods=['POST'])
def addWord():
    if request.method == "POST":
        french = request.form["fr"]
        normand = request.form['normand']

        if db.addWord(french,normand) == True:
            return jsonify(True)

@dict.route(f"{router}edit",methods=["POST"])
def updateWord():
    if request.method == "POST":
        id = request.form["id"]
        french = request.form["fr"]
        normand = request.form['normand']

        if db.updateWord(id,french,normand):
            return (f""" 
                <h1> Changement effectué ! </h1>
            """)
    

@dict.route(f"{router}delete",methods=["POST"])
def deleteWord():
    if request.method == "POST":
        id = request.form["id"]

    if db.getWord(id):
        if db.removeWord(id):
            return (f"""
                <h1>Le mot a été supprimé</h1>
            """)
        else:
            return(f"""
                <h1>Le mot n'a pas pu être supprimé de la base de donnée ou bien n'existe pas dans celle-ci ! </h1>
            """)

@dict.route(f"{router}search",methods=["POST"])
def searchWord():
    if request.method == "POST":
        word = request.form["word"]
        language = request.form["lang"]

    if db.word_exists(word) != False:
        match language:
            case "fr":
                return jsonify(db.getWord(db.word_exists(word))['fr'])
            case "normand":
                return jsonify(db.getWord(db.word_exists(word))['normand'])
            case _:
                return (jsonify(False))
    else:
        return (f""" 
            <h1> {word} n'a pas été trouvé ! </h1>
        """)

@dict.route(f"{router}",methods=["GET"])
def getAllWords():
    return jsonify(db.getAllWord())