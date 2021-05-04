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
    similarlist = None
    parentlist = None
    childlist = None
    relationlist = None
    nodetype = None
    relationtype = None

    if request.method == 'POST':
        input = request.form['chemical']
        type = request.form.get('choices-single-defaul')

        if type == "Not Specific":
            if input.upper().startswith('MESH') == True:
                node = myQuery.findNodebyID(input)
                if not node:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    if node.has_label('Disease'):
                        nodetype = 'Disease'
                        result_name = node['DiseaseName']
                        pmid_list = myQuery.findPaperGivenDisease(node)
                        paperlist = interface.getPaperInfobyID(pmid_list)
                        similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                        similarlist = interface.getPaperInfobyID(similar_pmid_list)
                        parentlist = myQuery.findDiseaseParent(node)
                        childlist = myQuery.findDiseaseChild(node)
                        relationlist = myQuery.findChemicalGivenDisease(node)
                    else:
                        nodetype = 'Chemical'
                        result_name = node['ChemicalName']
                        pmid_list = myQuery.findPaperGivenChemical(node)
                        paperlist = interface.getPaperInfobyID(pmid_list)
                        similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                        similarlist = interface.getPaperInfobyID(similar_pmid_list)
                        parentlist = myQuery.findChemicalParent(node)
                        childlist = myQuery.findChemicalChild(node)
                        relationlist = myQuery.findDiseaseGivenChemical(node)

            else:
                nodes = myQuery.findNodeContainName(input)
                if not nodes:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    if nodes[0].has_label('Disease'):
                        nodetype = 'Disease'
                        result_name = nodes[0]['DiseaseName']
                        parentlist = myQuery.findDiseaseParent(nodes[0])
                        childlist = myQuery.findDiseaseChild(nodes[0])
                        relationlist = myQuery.findChemicalGivenDisease(nodes[0])
                    else:
                        nodetype = 'Chemical'
                        result_name = nodes[0]['ChemicalName']
                        parentlist = myQuery.findChemicalParent(nodes[0])
                        childlist = myQuery.findChemicalChild(nodes[0])
                        relationlist = myQuery.findDiseaseGivenChemical(nodes[0])
                 #   result_name = nodes[0]
                    pmid_list = []
                    # iterate through nodes
                    for node in nodes:
                        pmid_list.extend(myQuery.findPaperGivenChemical(node))
                        pmid_list.extend(myQuery.findPaperGivenDisease(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)
                    similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                    similarlist = interface.getPaperInfobyID(similar_pmid_list)


        elif type == "Chemical":
            nodetype = 'Chemical'
            if input.upper().startswith('MESH')==True:
                query_result = myQuery.findChemicalbyID(input)

                # There is no result
                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    result_name = query_result['ChemicalName']
                    pmid_list = myQuery.findPaperGivenChemical(query_result)
                    paperlist = interface.getPaperInfobyID(pmid_list)
                    similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                    similarlist = interface.getPaperInfobyID(similar_pmid_list)
                    parentlist = myQuery.findChemicalParent(query_result)
                    childlist = myQuery.findChemicalChild(query_result)
                    relationlist = myQuery.findDiseaseGivenChemical(query_result)
            else:
                query_result = myQuery.findChemicalContainName(input, return_node=True)

                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    ## There is a list of nodes
                    # chemical names
                    result_name = query_result[0]['ChemicalName']
                    parentlist = myQuery.findChemicalParent(query_result[0])
                    childlist = myQuery.findChemicalChild(query_result[0])
                    relationlist = myQuery.findDiseaseGivenChemical(query_result[0])
                    # get the paper
                    pmid_list = []
                    # iterate through nodes
                    for node in query_result:
                        pmid_list.extend(myQuery.findPaperGivenChemical(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)
                    similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                    similarlist = interface.getPaperInfobyID(similar_pmid_list)


        elif type == "Disease":
            nodetype = 'Disease'
            if input.upper().startswith('MESH') == True:
                query_result = myQuery.findDiseasebyID(input)

                # There is no result
                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    result_name = query_result['DiseaseName']
                    pmid_list = myQuery.findPaperGivenDisease(query_result)
                    paperlist = interface.getPaperInfobyID(pmid_list)
                    similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                    similarlist = interface.getPaperInfobyID(similar_pmid_list)
                    parentlist = myQuery.findDiseaseParent(query_result)
                    childlist = myQuery.findDiseaseChild(query_result)
                    relationlist = myQuery.findChemicalGivenDisease(query_result)



            else:
                query_result = myQuery.findDiseaseContainName(input, return_node=True)

                if not query_result:
                    result_name = 'Not Found!'
                    paperlist = {}
                    similarlist = {}
                    parentlist = {}
                    childlist = {}
                    relationlist = {}
                else:
                    ## There is a list of nodes
                    # chemical names
                    result_name = query_result[0]['DiseaseName']
                    parentlist = myQuery.findDiseaseParent(query_result[0])
                    childlist = myQuery.findDiseaseChild(query_result[0])
                    relationlist = myQuery.findChemicalGivenDisease(query_result[0])
                    # get the paper
                    pmid_list = []
                    # iterate through nodes
                    for node in query_result:
                        pmid_list.extend(myQuery.findPaperGivenDisease(node))
                    # remove the duplicate pmid
                    pmid_list = list(set(pmid_list))
                    # get the full paper infos
                    paperlist = interface.getPaperInfobyID(pmid_list)
                    similar_pmid_list = interface.similar_paper(pmid_list, interface.represent_dict)
                    similarlist = interface.getPaperInfobyID(similar_pmid_list)
        if nodetype == 'Chemical':
            if parentlist and len(parentlist) > 5:
                parentlist = parentlist[:5]
            parentlist = [pnode['ChemicalName'] for pnode in parentlist]
            if childlist and len(childlist) > 5:
                childlist = childlist[:5]
            childlist = [cnode['ChemicalName'] for cnode in childlist]
            if relationlist and len(relationlist) > 5:
                relationlist = relationlist[:5]
            relationlist = [rnode['DiseaseName'] for rnode in relationlist]
            relationtype = 'Disease'
        elif nodetype == 'Disease':
            if parentlist and len(parentlist) > 5:
                parentlist = parentlist[:5]
            parentlist = [pnode['DiseaseName'] for pnode in parentlist]
            if childlist and len(childlist) > 5:
                childlist = childlist[:5]
            childlist = [cnode['DiseaseName'] for cnode in childlist]
            if relationlist and len(relationlist) > 5:
                relationlist = relationlist[:5]
            relationlist = [rnode['ChemicalName'] for rnode in relationlist]
            relationtype = 'Chemical'

    return render_template('list.html', chemical_name=result_name, paperlist = paperlist, similarlist = similarlist, parentlist = parentlist, childlist = childlist, relationlist = relationlist, nodetype = nodetype, relationtype = relationtype)


if __name__ == '__main__':
    app.run()
