import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher


#gene_file = '../../data_uiuc/genes.csv'
#disease_file = '../../data_uiuc/diseases.csv'
#gene_disease_file = '../../data_uiuc/genes_diseases_relation.csv'

chemical_file = '../../send/chemicals.csv'
disease_file = '../../send/diseases.csv'
chemical_disease_file = '../../send/chemicals_diseases_relation.csv'


chemical = pd.read_csv(chemical_file, sep='\t')
disease = pd.read_csv(disease_file, sep='\t')
chemical_disease = pd.read_csv(chemical_disease_file, sep='\t')

#node_info = disease.loc[1] # it has 'DiseaseID', 'DiseaseName', 'ParentID' fields
#def create_disease_node(node_info):
#    node = Node('Disease', DiseaseID = node_info[1], DiseaseName = node_info[0])
#    graph.create(node)

def create_disease_node(disease):
    """
    Create disease nodes in the graph database
    Disease (Node): label->"Disease", properties->{"DiseaseID","DiseaseName"}
    :param disease: pandas file
    :return: void
    """
    for i in range(len(disease)):
        node_info = disease.loc[i]
        node = Node('Disease', DiseaseID = node_info[1], DiseaseName = node_info[0])
        graph.create(node)
        #print("node",i)


def create_chemical_node(chemical):
    '''
    Create Chemical node in the graph
    Chemical Node: label('Chemical'), properties('ChemicalID', 'ChemicalName')
    :param chemical: chemical, pandas DataFrame
    :return: void
    '''
    for i in range(len(chemical)):
        node_info = chemical.loc[i]
        node = Node('Chemical', ChemicalID = node_info['ChemicalID'], \
                    ChemicalName = node_info['ChemicalName'])
        graph.create(node)


def create_diseaseParent_relation(disease):
    """
    create Relationship among child disease and parent disease
    with (Child, rel, Parent) triple
    :param disease: pandas read file
    :return: void
    """

    nodematcher = NodeMatcher(graph)
    ParentDisease = Relationship.type('ParentDisease')
    for i in range(len(disease)):
        node_info = disease.loc[i]

        # The node does not have parent
        if pd.isnull(node_info['ParentIDs']):
            continue
        # The node has parents
        this_node = nodematcher.match('Disease', DiseaseID = node_info['DiseaseID']).first()
        parent_list = node_info['ParentIDs'].split('|')
        #print(i,end='    ')
        for parent in parent_list:
            parent_node = nodematcher.match('Disease', DiseaseID = parent).first()
            # childNode -> parentNode
            # Possible error is that the parent node does not exist and will return None
            # I have not dealt with that case yet
            graph.create(ParentDisease(this_node, parent_node))
            #print(parent_node['DiseaseName'], end=' ')
        #print('\n')


def create_chemicalParent_relation(chemical):
    '''
    create Relationship among child chemical and parent chemical
    with (Child, rel, Parent) triple
    :param chemical: pandas read file
    :return: void
    '''
    nodematcher = NodeMatcher(graph)
    ParentChemical = Relationship.type('ParentChemical')
    for i in range(len(chemical)):
        node_info = chemical.loc[i]

        # The node does not have parent
        if pd.isnull(node_info['ParentIDs']):
            continue
        # The node has parents
        this_node = nodematcher.match('Chemical', ChemicalID=node_info['ChemicalID']).first()
        parent_list = node_info['ParentIDs'].split('|')
        # print(i,end='    ')
        for parent in parent_list:
            parent_node = nodematcher.match('Chemical', ChemicalID=parent).first()
            # childNode -> parentNode
            # Possible error is that the parent node does not exist and will return None
            # I have not dealt with that case yet
            graph.create(ParentChemical(this_node, parent_node))
            # print(parent_node['DiseaseName'], end=' ')
        # print('\n')

def create_ChemicalDisease_relation(chemical_disease):
    nodematcher = NodeMatcher(graph)
    ChemicalDisease = Relationship.type('ChemicalDisease')
    for i in range(len(chemical_disease)):
        rel_info = chemical_disease.loc[i]

        # if there is no pmids, i.e., there is no paper describing the relations, then drop
        if pd.isnull(rel_info['pmids']):
            continue

        # there is paper
        chemical_node = nodematcher.match('Chemical', ChemicalID=rel_info['ChemicalID']).first()
        disease_node = nodematcher.match('Disease', DiseaseID=rel_info['DiseaseID']).first()

        # if the rel nodes does not exist yet, then drop
        if(chemical_node==None or disease_node==None):
            continue

        # Create the relation, with (Chemical)->(Disease), property: pmids
        paper_list = rel_info['pmids'].split('|')
        chemical_disease_rel = ChemicalDisease(chemical_node, disease_node, pmids=paper_list)

        print(i)
        #put into the graph
        graph.create(chemical_disease_rel)



if __name__=='__main__':
    graph = Graph(password="syq4")
    #graph.schema.create_uniqueness_constraint("Disease","DiseaseID")
    # Following code is preserved
    '''
    graph.run("CREATE CONSTRAINT uniqueDisease ON (n:Disease) ASSERT n.DiseaseID IS UNIQUE")
    create_disease_node(disease)
    create_diseaseParent_relation(disease)
    
    graph.run("CREATE CONSTRAINT uniqueChemical ON (n:Chemical) ASSERT n.ChemicalID IS UNIQUE")
    create_chemical_node(chemical)
    create_chemicalParent_relation(chemical)
    
    create_ChemicalDisease_relation(chemical_disease)
    '''

    print('Hello main!')
    

