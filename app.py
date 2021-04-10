from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from GraphQueryClass import GraphQuery
import interface

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
    result_name = None
    paperlist = None

    if request.method == 'POST':
        input = request.form['chemical']
        type = request.form.get('choices-single-defaul')

        if type == "Not Specific":
            if input.upper().startswith('MESH') == True:
                node = myQuery.findNodebyID(input)
                if not node:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    if node.has_label('Disease'):
                        result_name = node['DiseaseName']
                        pmid_list = myQuery.findPaperGivenDisease(node)
                        paperlist = interface.getPaperInfobyID(pmid_list)
                    else:
                        result_name = node['ChemicalName']
                        pmid_list = myQuery.findPaperGivenChemical(node)
                        paperlist = interface.getPaperInfobyID(pmid_list)

            else:
                nodes = myQuery.findNodeContainName(input)
                if not nodes:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    if nodes[0].has_label('Disease'):
                        result_name = nodes[0]['DiseaseName']
                    else:
                        result_name = nodes[0]['ChemicalName']
                    result_name = nodes[0]
                    pmid_list = []
                    # iterate through nodes
                    for node in nodes:
                        pmid_list.extend(myQuery.findPaperGivenChemical(node))
                        pmid_list.extend(myQuery.findPaperGivenDisease(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)


        elif type == "Chemical":
            if input.upper().startswith('MESH')==True:
                query_result = myQuery.findChemicalbyID(input)

                # There is no result
                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    result_name = query_result['ChemicalName']
                    pmid_list = myQuery.findPaperGivenChemical(query_result)
                    paperlist = interface.getPaperInfobyID(pmid_list)
            else:
                query_result = myQuery.findChemicalContainName(input, return_node=True)

                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    ## There is a list of nodes
                    # chemical names
                    result_name = query_result[0]['ChemicalName']
                    # get the paper
                    pmid_list = []
                    # iterate through nodes
                    for node in query_result:
                        pmid_list.extend(myQuery.findPaperGivenChemical(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)


        elif type == "Disease":
            if input.upper().startswith('MESH') == True:
                query_result = myQuery.findDiseasebyID(input)

                # There is no result
                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    result_name = query_result['DiseaseName']
                    pmid_list = myQuery.findPaperGivenDisease(query_result)
                    paperlist = interface.getPaperInfobyID(pmid_list)

            else:
                query_result = myQuery.findDiseaseContainName(input, return_node=True)

                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                else:
                    ## There is a list of nodes
                    # chemical names
                    result_name = query_result[0]['DiseaseName']
                    # get the paper
                    pmid_list = []
                    # iterate through nodes
                    for node in query_result:
                        pmid_list.extend(myQuery.findPaperGivenDisease(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)

    return render_template('list.html', chemical_name=result_name, paperlist = paperlist)


if __name__ == '__main__':
    app.run()
