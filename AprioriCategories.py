
# coding: utf-8

# In[1]:


import sys
import random 
import threading
import random
import time
import re
import os

from collections import OrderedDict

# Step 1: Parse each line as a Transation with N elements which are split on ;
# Step 2: While parsing convert a unique string to a number for easy sorting 
# Step 3: 


def apriori(inputPath,relativeMinSupport) :
    
    transactions = [] # list of all transactions for use later
    lookup = {}
    totalLineCount = 0

    with open(inputPath) as f:
         for line in f:
            totalLineCount = totalLineCount + 1
#             print "line --> ", line
#             line = line.strip("\n\r")
#             print "line --> ", line
            data = re.split(';', line)
            transactions.append(data)
            # print "data --> ", data
            for i,category in enumerate(data): 
#                 print category
                category = category.rstrip()
                if category in lookup:
                    count = lookup[category]
                    count = count + 1
                    lookup[category] = count
                else:
                    lookup[category] = 1 

    print "Min Support:",int(totalLineCount * 0.01)

#   Remove k=1 without min support
    for category in lookup.keys():
        support = lookup[category]
        if support <= int(totalLineCount * 0.01):
            lookup.pop(category, None)

    #lookup is frequent-1 items

    printFrequent1Items(lookup)


def printFrequent1Items(lookup):
    if os.path.exists("patterns.txt"):
        os.remove("patterns.txt")
    f = open("patterns.txt", "a")
    for category in lookup:
        support = lookup[category]
        category = category.replace("\n", "")

        toWrite = str(support) + ":" + category

        f.write(toWrite)
        f.write("\n")
    f.close()


# In[2]:


apriori("categories.txt",1)

