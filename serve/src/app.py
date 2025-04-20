from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
import utils.dataUtils as dataUtils
import utils.pokeUtils as pokeUtils
import json
import random

app=Flask(__name__)
CORS(app)

PokeList=dataUtils.FileGetter('pokemon_full_list')
PokeList=pokeUtils.fliterPokeList(PokeList)
NameList=pokeUtils.OnlyNameGet(PokeList)
print(NameList)

@app.route('/debug',methods=["GET"])
def debug():
    return "debug"

@app.route('/initget',methods=["GET"])
def initget():
    hard=request.args.get('difficulty', default=0, type=int)
    gen=request.args.get('gen', default=0, type=int)
    return str(pokeUtils.getPokeByDf(PokeList,hard,gen))

@app.route('/nameget',methods=["GET"])
def nameget():
    return jsonify(NameList)

@app.route('/guess',methods=["GET"])
def guess():
    answer=request.args.get('answer', default=0, type=int)
    guess_id=request.args.get('guess', default=0, type=str)
    guess=pokeUtils.getPokeByName(PokeList,guess_id)
    if(answer==None or guess==None):
        return "guess name error"
    ans=pokeUtils.ComparePoke(PokeList,answer,guess)
    return jsonify(ans)

@app.route('/getimage',methods=["GET"])
def getimage():
    pokemon=request.args.get('pokemon', default=0, type=str)
    Id=pokeUtils.getPokeByName(PokeList,pokemon)
    path=PokeList[Id]["index"]+'-'+PokeList[Id]["name"]
    print(path)
    return send_file(dataUtils.SrcPath()+f'/data/images/official/{path}.png',mimetype='image/jpeg')

@app.route('/getanswer',methods=["GET"])
def getanswer():
    pokemon=request.args.get('pokemon', default=0, type=int)
    answer=pokeUtils.getPokeByName(PokeList,NameList[pokemon])
    if(answer==None):
        return "guess name error"
    ans=pokeUtils.ComparePoke(PokeList,answer,answer)
    return jsonify(ans)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9000)