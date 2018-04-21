from __future__ import print_function
import csv, math, random , sys



# To Split the data set in true and false
def splitSet(input_rows, column):
    trueSet = []
    falseSet = []
    for row in input_rows:
        if (row[column] == '0'):
            falseSet.append(row)
        else:
            trueSet.append(row)
    return (falseSet, trueSet)

# To Check Pure Class Value for that attribute label
def class_label(input_rows):  # finding the labels as 0's or 1's
    label = {}  # Dictionary creation
    label['1'] = 0
    label['0'] = 0
    for row in input_rows:
        lengthOfRow = len(row)
        attribute_class_label = row[lengthOfRow - 1]
        label[attribute_class_label] += 1
    return label

def probability(rows):
    labels = class_label(rows)
    p = 0.0
    for label in labels.keys():
        if len(rows) == 0:
            p = 0.0
        else:
            p = float(labels[label]) / float(len(rows))
    return p


# function to calculate Entropy
def entropy(rows):
    from math import log
    ent = 0.0
    pi = probability(rows)
    # importing the probability from the above probability function
    if (pi == 0.0):
        ent = 0.0
    else:
        ent = ent - pi * math.log(pi, 2)
    return ent

# function to calculate information gain
def InformationGain(rows, columncount):
    max_gain = 0.0
    gain = 0.0
    valid = 0
    for attribute_index in range(0, columncount):
        falseSet, trueSet = splitSet(rows, attribute_index)
        q = float(len(trueSet)) / float(len(rows))
        # calculating the weighted probability
        p = float(len(falseSet)) / float(len(rows))
        if (len(falseSet) > 0 and len(trueSet) < 0):
            return -1
        elif (len(falseSet) < 0 and len(trueSet) > 0):
            return -1
        elif (len(falseSet) < 0 and len(trueSet) < 0):
            return -1
        else:
            child_Entropy = (p * entropy(falseSet) + q * entropy(trueSet))
            gain = entropy(rows) - child_Entropy
            if (gain > max_gain):
                # choosing the best split by calculating the maximum information gain
                max_gain = gain
                position = attribute_index
                valid = 1

    if (valid == 1):
        return position
    else:
        return -1  # When no information gain and we can'tsplit further

#Define class
class decisionnode:
        def __init__(self, col=-1, pure=None, value=None, parentlist=set(), leftchild=None, rightchild=None,
                     number=None, name=None, count=None, nodes=None, noof0=0, noof1=0, parent=None):
            self.leftchild = leftchild
            self.rightchild = rightchild
            self.number = number
            self.name = name
            self.nodes = nodes
            self.col = col
            self.pure = pure
            self.value = value
            self.noof1 = noof1
            self.noof0 = noof0
            self.parent = parent
            self.parentlist = parentlist


#To Select Random attribute
def randomselect(rows,parentlist,attributelength):
    j = 1
    parlist = len(parentlist)
    Indexlist = parentlist
    while (j > 0 and len(Indexlist) < 20):
        Index = random.randint(0,(attributelength - 1 ))
        if(Index not in Indexlist):
            falseSet,trueSet  = splitSet(rows,Index)
            if(len(falseSet) > 0 and len(trueSet) > 0):
                j = 0
            else:
                Indexlist = Indexlist | {Index}
    #print("Index list is      : ",Indexlist)
    if(len(Indexlist) == attributelength):     
        return -1
    else:
        return Index

#build tree with random attributes
def randomTree(rows,attributelength,val,parentlist):
    global nodes
    global leafcount                              
    if len(rows)==0:
        nodes  = nodes + 1
        return decisionnode()
    
    #print("random select is ",parentlist)
    #print("parentlis is before:",parentlist)
    Index = randomselect(rows,parentlist,attributelength)
    #print("parentlis is after:",parentlist)

    if(Index == -1):
        if(class_label(rows)['0'] > class_label(rows)['1']):
            value = 0
            nodes = nodes + 1
            leafcount = leafcount + 1
            return decisionnode( pure= class_label(rows),value = value,nodes= nodes,noof0 = class_label(rows)['0'])
        else :
            value = 1
            nodes = nodes + 1
            leafcount = leafcount + 1
            return decisionnode(pure= class_label(rows),value = value,nodes = nodes, noof1 =  class_label(rows)['1'])
    else:
        falseSet,trueSet  = splitSet(rows,Index)
        nodes = nodes + 1
        temp = decisionnode(col = attributes[Index],value = val, number = Index,parentlist = parentlist, nodes = nodes,noof0 = class_label(rows)['0'],noof1 = class_label(rows)['1'])
        if(len(trueSet) > 0):
            rightchild = randomTree(trueSet,attributelength ,1,temp.parentlist | {temp.number})
            temp.rightchild = rightchild
            rightchild.parent = temp
            rightchild.parentlist = temp.parentlist | {temp.number}
        if(len(falseSet) > 0):
            leftchild  = randomTree(falseSet,attributelength ,1,temp.parentlist | {temp.number})
            temp.leftchild = leftchild
            leftchild.parent = temp
            leftchild.parentlist = temp.parentlist | {temp.number}
        return temp

def ID3Tree(rows,attributelength,val,parentlist):
    global nodes
    global leafcount                              
    if len(rows)==0:
        nodes  = nodes + 1
        return decisionnode()
    Index = InformationGain(rows,attributelength)
    if(Index == -1):
        if(class_label(rows)['0'] > class_label(rows)['1']):
            value = 0
            nodes = nodes + 1
            leafcount = leafcount + 1
            return decisionnode( pure= class_label(rows),value = value,nodes = nodes,noof0 = class_label(rows)['0'])
        else :
            value = 1
            nodes = nodes + 1
            leafcount = leafcount + 1
            return decisionnode(pure= class_label(rows),value = value,nodes = nodes, noof1 =  class_label(rows)['1'])
    else:
        falseSet,trueSet  = splitSet(rows,Index)
        nodes = nodes + 1
        temp = decisionnode(col = attributes[Index],value = val, number = Index, nodes = nodes,noof0 = class_label(rows)['0'],noof1 = class_label(rows)['1'])

        if(len(trueSet) > 0):
            rightchild = ID3Tree(trueSet,attributelength ,1,temp.parentlist | {temp.number})
            temp.rightchild = rightchild
            rightchild.parent = temp
            rightchild.parentlist = temp.parentlist | {temp.number}

        if(len(falseSet) > 0):
            leftchild  = ID3Tree(falseSet,attributelength ,1,temp.parentlist | {temp.number})
            temp.leftchild = leftchild
            leftchild.parent = temp
            leftchild.parentlist = temp.parentlist | {temp.number}        
        nodes = nodes + 1    
        #print(temp.col)
        return temp
def TotalNodes(tree):
    count = 1
    if(tree is None):
        return 0
    if(tree is not None):
        count = count + TotalNodes(tree.rightchild)
        count = count + TotalNodes(tree.leftchild)
    return count

def Numbering(tree,count):
    if(tree is None):
        return count
    if(tree.pure is not None):
        tree.nodes = 0
        return count
    if(tree is not None):
        count = count + 1;
        tree.nodes = count
        count = Numbering(tree.rightchild,count)
        count = Numbering(tree.leftchild,count)
    return count

def leafcounts(tree1,tree,count,totaldepth):
    
    #print(tree.pure)
    if(tree is None):
        return (0,0)
    if(tree.pure is not None):
        d = finddepth(tree1,tree.nodes,0)
        return (1,d)
    else:
        lc,ld = leafcounts(tree1,tree.leftchild,count,totaldepth)
        rc,rd = leafcounts(tree1,tree.rightchild,count,totaldepth)
        count = count + lc + rc
        totaldepth = totaldepth + rd + ld
        return (count,totaldepth)
def depth(tree):
    depth1 = 0
    depth2 = 0
    if(tree is None):
        return 0
    else:
        depth1 = 1 + depth(tree.rightchild)
        depth2 = 1 + depth(tree.leftchild)
        if(depth1 > depth2):
            return depth1
        else:
            return depth2

def printtree(tree,bar=''):
    if tree.pure!=None:
        if(tree.pure['0'] > tree.pure['1']):
            print(0)
        else:
            print(1)
    else:
        #print(str(tree.col)+':'+str(tree.value)+'? ')

        print('\n' + bar,str(tree.col)+' = '+str(1), end=": ")
        printtree(tree.rightchild,bar+'| ')
        if(tree.value == 1):
            val = 0
        else:
            val = 1    
        print(bar,str(tree.col)+' = '+str(0), end=": ")
        printtree(tree.leftchild,bar+'| ')

def classify(newinput,tree):
    if tree.pure!=None:
        #print(tree.pure)
        return tree.pure
    else:
        v= newinput[tree.number]
        #print ('v is ',v,newinput[tree.number],' and tree index is ', tree.number)
        branch=None
        if v == '1':
            branch = tree.rightchild
            if(branch is None):
                branch = tree.leftchild
        else:
            branch=tree.leftchild
            if(branch is None):
                branch = tree.rightchild
    return classify(newinput,branch)

def Accuracy(data,tree):
    count = 0
    temp = -1
    for row in data:
        temp = temp + 1
        if(classify(row,tree)['1'] >= classify(row,tree)['0'] ):
            if(row[-1] == '1'):
                count = count + 1
        else:
            if row[-1] == '0':
                count = count + 1
    #print(count,' - count ; total',len(data))
    acc = count/float(len(data))
    return acc
def findNode(tree,nodes):
    node = None
    if(tree is None):
        return None
    elif(tree.nodes == nodes):
        return tree

    if(tree is not None):
        node = findNode(tree.rightchild,nodes)
        if(node is None):
            node = findNode(tree.leftchild,nodes)
    return node
def finddepth(tree,number,depth):
    if (tree is None):
        return 0
    elif (tree.nodes == number):
        return depth
 
    downlevel = finddepth(tree.leftchild, number, depth+1);
    if (downlevel != 0):
        return downlevel
    downlevel = finddepth(tree.rightchild, number, depth+1);
    return downlevel

def findparent(tree):
    if(tree is None):
        return None
    elif(tree.parent is not None):
        return findparent(tree.parent)
    else:
        return tree

def main():

    test_cases = []
    test_attributes = []

    validation_cases = []
    validation_attributes = []
    with open (sys.argv[2],'r') as csvfile:
        reader2 = csv.reader(csvfile)
        validation_attributes =next(reader2)
        for row in reader2:
            validation_cases += [row]
        csvfile.close()
    with open (sys.argv[3],'r') as csvfile:
        reader1 = csv.reader(csvfile)
        test_attributes =next(reader1)
        for row in reader1:
            test_cases += [row]
        csvfile.close()
    with open (sys.argv[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        train_cases = []
        firstline = next(reader)
        global attributes
        global nodes
        global leafcount
        nodes =0
        leafcount = 0
        attributes = {}
        attribute_values = []
        total_cases = []
        i = 0
        for column in firstline[0:-1]:
            attributes[i] = column
            i = i +1
            #print column
        #print attributes
        attribute_values = {'0','1'}
        #print len(attributes)
        for row in reader:
            total_cases += [row]
            case = (row[0:-1], row[-1])
            train_cases += [case]
        attributes_left = []
        for i in range(0,len(attributes)):
            attributes_left = attributes_left + [i]
        j = 1
        while (j > 0):
            j = 0
            tree=ID3Tree(total_cases,len(attributes),1,set())
            print('----------------------------------------------------------------------------------\n')
            print('Pre-Pruned Accuracy of ID3 Selection')
            print('-------------------')
            print('Number of training instances = ',len(total_cases))
            print('Number of training attributes = ',len(attributes))
            print('Total number of nodes in the tree = ',TotalNodes(tree))
            print('Number of leaf nodes in the tree = ',leafcounts(tree,tree,0,0)[0])
            print('Average Depth of leaf nodes in the tree = ',float(leafcounts(tree,tree,0,0)[1])/leafcounts(tree,tree,0,0)[0])
            train_accuracy = Accuracy(total_cases,tree)
            print('Accuracy of the model on the training dataset = ',train_accuracy*100,'%\n\n')

            pre_validation_accuracy = Accuracy(validation_cases,tree)   
            print('Number of validation instances = ',len(validation_cases))
            print('Number of validation attributes = ',len(validation_attributes) - 1)
            print('Accuracy of the model on the validation dataset before pruning = ',pre_validation_accuracy*100,'%\n\n')   

            test_accuracy = Accuracy(test_cases,tree)
            print('Number of testing instances = ',len(test_cases))
            print('Number of testing attributes = ',len(test_attributes) - 1)
            print('Accuracy of the model on the testing dataset = ',test_accuracy*100,'%')
            print('----------------------------------------------------------------------------------\n')
            cont1 = input("Print ID3 Decision Tree ? select  yes/no ?    :")
            if cont1 == "yes":
                printtree(tree)



            randtree=randomTree(total_cases,len(attributes),1,set())
            print('----------------------------------------------------------------------------------\n')
            print('Pre-Pruned  of Random Selection')
            print('-------------------')
            print('Number of training instances = ',len(total_cases))
            print('Number of training attributes = ',len(attributes))
            print('Total number of nodes in the tree = ',TotalNodes(randtree))
            print('Number of leaf nodes in the tree = ',leafcounts(randtree,randtree,0,0)[0])
            print('Average Depth of leaf nodes in the tree = ',float(leafcounts(randtree,randtree,0,0)[1])/leafcounts(randtree,randtree,0,0)[0])
            train_accuracy = Accuracy(total_cases,randtree)
            print('Accuracy of the model on the training dataset '
                  '= ',train_accuracy*100,'%\n\n')

            pre_validation_accuracy = Accuracy(validation_cases,randtree)   
            print('Number of validation instances = ',len(validation_cases))
            print('Number of validation attributes = ',len(validation_attributes) - 1)
            print('Accuracy of the model on the validation dataset before pruning = ',pre_validation_accuracy*100,'%\n\n')   

            test_accuracy = Accuracy(test_cases,randtree)
            print('Number of testing instances = ',len(test_cases))
            print('Number of testing attributes = ',len(test_attributes) - 1)
            print('Accuracy of the model on the testing dataset = ',test_accuracy*100,'%')
            print('----------------------------------------------------------------------------------\n')
            cont2 = input("Print RandomSelect Decision Tree ? select  yes/no    ?")
            if cont2 == "yes":
                printtree(randtree)

if __name__ == "__main__":
    main()
