
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
    frequentKItems = {}
    totalLineCount = 0

    with open(inputPath) as f:
         for line in f:
            totalLineCount = totalLineCount + 1
            line = line.rstrip()
            data = re.split(';', line)
            transactions.append(data)
            # print "data --> ", data
            for i,category in enumerate(data): 
#               print category
                if category in frequentKItems:
                    count = frequentKItems[category]
                    count = count + 1
                    frequentKItems[category] = count
                else:
                    frequentKItems[category] = 1

    if relativeMinSupport is None :
        relativeMinSupport = int(totalLineCount * 0.01)

    print frequentKItems

    print "Min Support:",relativeMinSupport

#   Remove k=1 without min support
    for category in frequentKItems.keys():
        support = frequentKItems[category]
        if support <= relativeMinSupport:
            frequentKItems.pop(category, None)

    print frequentKItems

    # printFrequentItems(frequentKItems,"frequent1Items.txt")

    frequen1Items = []
    for aFreq1Itemcategory in frequentKItems.keys():
        frequen1Items.append(aFreq1Itemcategory)

    k=2
    allKItemSetsToFind = getKItemCombinations(frequen1Items, k)


def getKItemCombinations(frequen1Items, k):
    x=1
    allKItemSetsToFind = []
    for i, category in enumerate(frequen1Items):
        itemsToFind = []
        itemsToFind.append(category)
        for j, category2 in enumerate(frequen1Items):
            if j > i:
                x = x + 1
                if x <= k:
                    itemsToFind.append(category2)
                    if x == k:
                        if len(itemsToFind) == k:
                            allKItemSetsToFind.append(itemsToFind)
                            itemsToFind = []
                            itemsToFind.append(category)
                            x = 1
        x = 1

    print "k = ",k,"--> ",allKItemSetsToFind

    return allKItemSetsToFind


def printFrequentItems(printFrequentItems,fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
    f = open(fileName, "a")
    for category in printFrequentItems:
        support = printFrequentItems[category]
        category = category.replace("\n", "")

        toWrite = str(support) + ":" + category

        f.write(toWrite)
        f.write("\n")
    f.close()


# In[2]:


# apriori("categories.txt",None)
apriori("test_cats.txt",2)

