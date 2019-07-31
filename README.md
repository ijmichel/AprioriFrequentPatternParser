# AprioriFrequentPatternParser

Created this project for a coursera assignment.  Apriori that goes until it can't find anymore frequent patterns, then outputs them to a file.  Run it using:

apriori("categories.txt",None) 

This makes it so the support threshold is 0.1 percent of the total # of transactions.

apriori("test_cats.txt",2)

This is a test set of patterns to find used during development for speed, which sets support to 2
