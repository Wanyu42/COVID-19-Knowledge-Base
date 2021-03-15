from py2neo import Graph
from py2neo.matching import *

def findDiseasebyID(DiseaseID):
    '''
    find Disease Node by DiseaseID
    :param DiseaseID: string type
    :return: Node type
    '''
    return nodematcher.match('Disease', DiseaseID=DiseaseID).first()

def findChemicalbyID(ChemicalID):
    '''
    find Chemical Node by ChemicalID
    :param ChemicalID: string type
    :return: Node type
    '''
    return nodematcher.match('Chemical', ChemicalID=ChemicalID).first()

def findDiseaseParent(DiseaseNode):
    '''
    get a list of parents of the Disease Node
    :param DiseaseNode: Node type
    :return: a list contains Parents Node
    '''
    rel_list = relmatcher.match([DiseaseNode, None], r_type='ParentDisease').all()
    parent_list = [rel.end_node for rel in rel_list]
    return parent_list

def findDiseaseChild(DiseaseNode):
    '''
    get a list of children of the current disease node
    :param DiseaseNode: Node type
    :return: a list of Node type
    '''
    rel_list = relmatcher.match([None, DiseaseNode], r_type='ParentDisease').all()
    child_list = [rel.start_node for rel in rel_list]
    return child_list

def findChemicalParent(ChemicalNode):
    '''
    get a list parents of the current chemical node
    :param ChemicalNode: Node type
    :return: a list of Node type
    '''
    rel_list = relmatcher.match([ChemicalNode, None], r_type='ParentChemical').all()
    parent_list = [rel.end_node for rel in rel_list]
    return parent_list

def findChemicalChild(ChemicalNode):
    '''
    get a list of children of the current chemical node
    :param ChemicalNode: Node type
    :return: a list of Node type
    '''
    rel_list = relmatcher.match([None, ChemicalNode], r_type='ParentChemical').all()
    child_list = [rel.start_node for rel in rel_list]
    return child_list

def findPaperGivenChemical(ChemicalNode):
    '''
    Retrieve the list of papers containing the chemical node
    :param ChemicalNode: Node type
    :return: a list of list with the first column describes the disease
            (Disease Node), the second column be string 'pmids'
    '''
    rel_list = relmatcher.match([ChemicalNode, None], r_type='ChemicalDisease')
    paper_list = [ [rel.end_node, rel.get('pmids')] for rel in rel_list]
    return paper_list

def findPaperGivenDisease(DiseaseNode):
    '''
    Retrieve the list of papers containing the desease node
    :param DiseaseNode: Node type
    :return: a list of list with the first column being Chemical Node that
            has effect on the disease, and the second column being the paper with 'pmids'
    '''
    rel_list = relmatcher.match([None, DiseaseNode], r_type='ChemicalDisease')
    paper_list = [ [rel.start_node, rel.get('pmids')] for rel in rel_list]
    return paper_list

def findPaperGivenPair(ChemicalNode, DiseaseNode):
    '''
    Retrieve the pmids of papers given the chemical and disease nodes
    :param ChemicalNode: Node type
    :param DiseaseNode: Node type
    :return: a list of strings
    '''
    rel_list = relmatcher.match([ChemicalNode, DiseaseNode], r_type='ChemicalDisease')
    paper_list = [rel.get('pmids') for rel in rel_list]
    return paper_list

def findDiseaseContainName(DiseaseName):
    '''
    find the disease Node containing the name string
    :param DiseaseName: string type
    :return: list of Node type
    '''
    return nodematcher.match('Disease', DiseaseName=CONTAINS(DiseaseName)).all()

def findChemicalContainName(ChemicalName):
    '''
    find the chemical Node containing the name string
    :param ChemicalName: string type
    :return: list of Node type
    '''
    return nodematcher.match('Chemical', ChemicalName=CONTAINS(ChemicalName)).all()


# main for test
if __name__ == "__main__":
    print("Hello GraphQuery")

    graph = Graph(password='syq4')
    nodematcher = NodeMatcher(graph)
    relmatcher = RelationshipMatcher(graph)


    # test cases
    '''
    test_node = findDiseasebyID('MESH:D058489')
    child_of_test = findDiseaseChild(test_node)
    print(len(child_of_test))
    
    # test case for chemical node
    
    test_chemical = findChemicalbyID('MESH:D019307')
    print(test_chemical)
    child_of_test_chemical = findChemicalChild(test_chemical)
    print(len(child_of_test_chemical))
    #print(child_of_test_chemical[0].end_node)
    
    # test case for paper given chemical
    
    test_chemical = findChemicalbyID('MESH:C534883')
    print(test_chemical)
    paper_of_chemical = findPaperGivenChemical(test_chemical)
    #print(paper_of_chemical[:][1])
    # Retrieve the whole papers
    column = list(zip(*paper_of_chemical))
    print(column[1][10])
    

    # test case for paper given disease
    
    test_disease = findDiseasebyID('MESH:D058489')
    print(test_disease)
    paper_of_disease = findPaperGivenDisease(test_disease)
    print(len(paper_of_disease)) # 456 papers
    

    # test case for paper given pair
    
    test_disease = findDiseasebyID('MESH:D011471')
    test_chemical = findChemicalbyID('MESH:C534883')
    paper_pair = findPaperGivenPair(test_chemical, test_disease)
    print(paper_pair)
    
    # test string match for disease
    test_disease_name = 'Disorders of Sex Development'
    print(findDiseaseContainName(test_disease_name))
    
    # test string match for chemical
    test_chemical_name = 'Isoquino'
    test_chemical_node_list = findChemicalContainName(test_chemical_name)
    for node in test_chemical_node_list:
        print(node.get('ChemicalID'))
    '''

    print("Goodbye GraphQuery")