from GraphQueryClass import GraphQuery
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import re

def findParentSubgraph(Node):
    if Node.has_label('Chemical'):
        parent_list = myQuery.findChemicalParent(Node)
        return [(Node['ChemicalID'], parent['ChemicalID']) for parent in parent_list]
    else:
        parent_list = myQuery.findDiseaseParent(Node)
        return [(Node['DiseaseID'], parent['DiseaseID']) for parent in parent_list]

def findChildSubgraph(Node):
    if Node.has_label('Chemical'):
        child_list = myQuery.findChemicalChild(Node)
        return [(child['ChemicalID'], Node['ChemicalID'] ) for child in child_list]
    else:
        child_list = myQuery.findDiseaseChild(Node)
        return [(child['DiseaseID'], Node['DiseaseID'] ) for child in child_list]

def findSubgraph(Node):
    parent_list = findParentSubgraph(Node)
    child_list = findChildSubgraph(Node)
    if Node.has_label('Chemical'):
        opposite_list = myQuery.findSubgraphFromChemical(Node)
    else:
        opposite_list = myQuery.findSubgraphFromDisease(Node)
    return [*parent_list, *child_list, *opposite_list]

def getPaperInfobyID(pmid_list):
    """
    Get the information of papers in the pmid_list
    :param pmid_list: a list of pmid
    :return: a dictionary of {key:pmid, value:paper info}
    """
    conn = sqlite3.connect('paper_list.db')
    cursor = conn.cursor()
    select_sql = '''SELECT * FROM PAPER_LIST WHERE PMID={}'''
    papers = {}
    for pmid in pmid_list:
        cursor.execute(select_sql.format(pmid))
        paper_info = cursor.fetchone()
        # The paper does not exist
        if paper_info == None:
            continue
        # The paper exists
        else:
            paper_dict = {}
            # Get the paper info
            if paper_info[1]==None:
                paper_dict['doi'] = ''
            else:
                paper_dict['doi'] = paper_info[1]
            paper_dict['title'] = paper_info[2]
            paper_dict['authors'] = paper_info[3]
            paper_dict['year'] = re.search('\d{4}', paper_info[4]).group(0)
            paper_dict['citedby'] = paper_info[5].split('|')
            paper_dict['abstract'] = paper_info[6]

            papers[paper_info[0]] = paper_dict

    conn.close()
    return papers


if __name__ == "__main__":
    myQuery = GraphQuery(30)

    '''
    test_chemical = myQuery.findChemicalbyID('MESH:D019307')

    subgraph_list = findSubgraph(test_chemical)
    test_G = nx.DiGraph()
    test_G.add_edges_from(subgraph_list)
    nx.draw_shell(test_G, node_size=1)
    plt.show()
    '''

    test_chemical = myQuery.findChemicalbyID('MESH:D019307')
    paper_list = myQuery.findPaperGivenChemical(test_chemical)

    papers = getPaperInfobyID(paper_list)

