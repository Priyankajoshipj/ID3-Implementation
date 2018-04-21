# ID3-Implementation
ID3 Algorithm impementation in python
Abstract

ID3 Algorithm is used in this assignment to select the best attribute in the process of building a decision tree. Decision tree classifies instances by sorting them from the root node to the leaf node following a path based on true or false values of different attributes. Each path of the classifier gives a rule to classify new data that is given as an input to it. Now, which attribute is the best fit for splitting the data set first and how do we proceed? To get a solution for these questions we have used ID3 Algorithm.

ID3 Algorithm
ID3 Algorithm uses a statistical property known as Information gain to measure how well an attribute splits the training data according to their target classification. To calculate information Gain we should be familiar with entropy which can be defined as a degree of chaos in the data sample, that is the degree of impurity of a data set. Entropy can be described as:

Entropy(S) =  -p(I) log2 p(I)
Where, p+ is the proportion of positive examples in the dataset and
 p- is the proportion of negative examples in the dataset

Information gain is the measure of effectiveness an attribute has to separate the positive and negative instances correctly.
Gain(S, A) = Entropy(S) -  ((|Sv| / |S|) * Entropy(Sv))

Where, Sv is the set of values of A
The attribute with the highest Information gain is chosen as the root node and the data set splits into subsets and the process is repeated until we get all pure nodes.
The tree stops to split the dataset if one among the following two situations arise
•	The attributes are all used up to split the data and still not all leaf nodes are pure
•	The data has been used up

After training the classifier with training data, it is tested on another dataset known as validation data and accuracy is calculated after each stage of training, validating and testing of the classifier.
Accuracy can be defined as the measure of correctly classified instances in a data set.
Accuracy = (Number of instances correctly classified)/(Total number of instances)

Pruning: To avoid the most common problem of overfitting in machine learning we have used the approach that allow the tree to overfit the data, and then post-prune the tree. The process of removing some random nodes from a tree is known as pruning. The number of nodes to be pruned is determined by the pruning factor. 
Number of nodes to be pruned = pruning factor * total number of nodes

Assumptions

While doing the assignment, we assumed the following:
1.	log20 = 0
2.	All the attributes had binary outputs.
3.	After constructing a tree, if there is a leaf node that contains data from more than 1 class i.e. it is not a pure node, then we chose the most frequent class in that node and output that as the predicted class.

Observations

1.	The classifier had a high accuracy on the training data.
2.	The accuracy of was increased after pruning from 74.8% to 75.35%
3.	The accuracy of the model was more on the training set than on testing set.

Accomplishment and Learning

After a lot of research and analysis we accomplished creating the decision tree with the given dataset and calculate accuracy, number of leaf nodes, depth of the tree and other measures for training dataset, validation dataset and testing dataset.

We learned concepts of ID3 algorithm thoroughly while working on this assignment. We also learned the role of the pruning process in increasing the accuracy of the model created.
