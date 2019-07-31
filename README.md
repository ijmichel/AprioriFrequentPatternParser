# AprioriFrequentPatternParser

Created this project for a coursera assignment.  This code is an implemenation of the famout Apriori (https://en.wikipedia.org/wiki/Apriori_algorithm) algorithm.  The algorithm will find all frequent items in a set of transactions.  It outputs the patterns to a file with the following format:

support:category1;category2;...
...

Run the code with the two sample input files using:

apriori("categories.txt",None) 

This makes it so the support threshold is 0.1 percent of the total # of transactions.

Or this sample input file:

apriori("test_cats.txt",2)

This is a test set of patterns to find used during development for speed, which sets support to 2
