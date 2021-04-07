from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from GraphQueryClass import GraphQuery


app = Flask(__name__)
myQuery = GraphQuery()

'''
@app.route('/')
def hello():
    query_result = myQuery.findChemicalbyID('MESH:D019307')
    return query_result['ChemicalName']
'''

@app.route('/', methods=['POST','GET'])
def init():
    chemical_name = None
    paperlist = None
    if request.method == 'POST':
        chemical = request.form['chemical']
        query_result = myQuery.findChemicalbyID(chemical)
        if query_result == None:
            chemical_name ='Chemical Not Found!'
            paperlist = ['Paper Not Found!']
        else:
            chemical_name = query_result['ChemicalName']
            paper_of_chemical = myQuery.findPaperGivenChemical(query_result)
            column = list(zip(*paper_of_chemical))
            paperlist = sum(column[1],[])
    return render_template('init.html', chemical_name=chemical_name, paperlist = paperlist)


if __name__ == '__main__':
    app.run()
