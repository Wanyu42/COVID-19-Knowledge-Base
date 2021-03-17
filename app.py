from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from GraphQueryClass import GraphQuery


app = Flask(__name__)
myQuery = GraphQuery()
Dict = {'a': 1, 'b': 2, 'c': 3 , 'd': 4}

'''
@app.route('/')
def hello():
    query_result = myQuery.findChemicalbyID('MESH:D019307')
    return query_result['ChemicalName']
'''

@app.route('/', methods=['POST','GET'])
def init():
    chemical_name=None
    if request.method == 'POST':
        chemical = request.form['chemical']
        query_result = myQuery.findChemicalbyID(chemical)
        if query_result == None:
            chemical_name ='Chemical Not Found!'
        else:
            chemical_name = query_result['ChemicalName']
    return render_template('init.html', chemical_name=chemical_name)


if __name__ == '__main__':
    app.run()
