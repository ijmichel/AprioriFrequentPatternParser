import re
import os


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
                if category in frequentKItems:
                    count = frequentKItems[category]
                    count = count + 1
                    frequentKItems[category] = count
                else:
                    frequentKItems[category] = 1

    if relativeMinSupport is None :
        relativeMinSupport = int(totalLineCount * 0.01)

    # print frequentKItems

    # print "Min Support:",relativeMinSupport

    f = None

    frequentKItems = filterItemSetByMinSupport(frequentKItems, relativeMinSupport)
    f = printFrequentItems(frequentKItems, "frequentKItems.txt",f,False,True)
    frequen1Items = getFrequentLabels(frequentKItems)


    kItemSets = getKEquals1combinations(frequen1Items)

    k=2
    while True:
        kItemsWithSupport = getKItemsWithSupport(kItemSets,transactions)
        kFreqItemSets = filterItemSetByMinSupport(kItemsWithSupport,relativeMinSupport)

        # def printFrequentItems(printFrequentItems, fileName, f, close, removeFirst):

        if len(kFreqItemSets) == 0:
            break
        else:
            f = printFrequentItems(kFreqItemSets, "frequentKItems.txt",f,False,False)
            kFreqItemLabels = getFrequentLabels(kFreqItemSets)

        kItemSets = getNextItemCombinations(frequen1Items,kFreqItemLabels)
        k = k + 1


    if f is not None:
        f.close()


def getNextItemCombinations(frequen1Items, kFreqItemSets):

    permutaitonsAll = ()
    for itemSetToCombine in kFreqItemSets:
        permuationGo = ()
        toCombine = itemSetToCombine.itemSet
        for oneItem in frequen1Items:
            if not oneItem in toCombine:
                permuationGo = toCombine[:]
                permuationGo = permuationGo + (oneItem,)
                permutaitonsAll = permutaitonsAll + (permuationGo,)

    return permutaitonsAll



def filterItemSetByMinSupport(frequentKItems, relativeMinSupport):
    #   Remove k=1 without min support
    for category in frequentKItems.keys():
        support = frequentKItems[category]
        if support <= relativeMinSupport:
            frequentKItems.pop(category, None)
    print frequentKItems
    return frequentKItems

def getFrequentLabels(frequentKItems):
    frequenKItems = ()
    for aFreq1Itemcategory in frequentKItems.keys():
        frequenKItems = frequenKItems + (aFreq1Itemcategory,)
    return frequenKItems



def getKItemsWithSupport(kItemSets,transactions):
    kItemSetToSupport = {}
    for itemSet in kItemSets:
        aItemSet = itemSet
        if isinstance(itemSet,ItemSet) :
            aItemSet = itemSet.itemSet
        support = 0
        for trnx in transactions:
            lToF = len(aItemSet)
            c = 0
            for j,item in enumerate(aItemSet):
                for i, category in enumerate(trnx):
                    if category == item:
                        c = c + 1

            if c==lToF: #found itemset in transaction
                support = support + 1

        # print "before : " + str(aItemSet) + " after : " + str(sorted(aItemSet))
        sorted(aItemSet)
        itemSetCll = ItemSet(aItemSet)

        if itemSetCll not in kItemSetToSupport:
            kItemSetToSupport[itemSetCll] = support

    return kItemSetToSupport


class ItemSet:
    def __init__(self, itemSet):
        self.itemSet = itemSet

    def __repr__(self):
        return str(self.itemSet)


def getKEquals1combinations(frequen1Items):
    k=2
    x=1
    allKItemSetsToFind = ()

    for i, category in enumerate(frequen1Items):
        itemsToFind = ()
        itemsToFind = itemsToFind + (category,)
        for j, category2 in enumerate(frequen1Items):
            if j > i:
                x = x + 1
                if x <= k:
                    itemsToFind = itemsToFind + (category2,)
                    if x == k:
                        if len(itemsToFind) == k:
                            allKItemSetsToFind = allKItemSetsToFind + (itemsToFind,)
                            itemsToFind = ()
                            itemsToFind = itemsToFind + (category,)
                            x = 1
        x = 1

    # print "k = ",k,"--> ",allKItemSetsToFind

    return allKItemSetsToFind


def printFrequentItems(printFrequentItems,fileName,f,close,deleteIt):

    if deleteIt:
        if os.path.exists(fileName):
            os.remove(fileName)

    if f is None:
        f = open(fileName, "a")

    for category in printFrequentItems:
        support = printFrequentItems[category]
        toWrite = str(support) + ":"

        if isinstance(category,ItemSet):
            catList = category.itemSet
            if isinstance(catList, tuple):
                l = len(catList)
                i=1
                for aCat in catList:
                    aCat = aCat.replace("\n", "")
                    if i != l:
                        toWrite = toWrite + aCat + ";"
                    else:
                        toWrite = toWrite + aCat
                    i = i + 1
        else:
            category = category.replace("\n", "")
            toWrite = toWrite + category

        f.write(toWrite)
        f.write("\n")

    if close:
        f.close()

    return f


# In[2]:


#apriori("categories.txt",None)
apriori("test_cats.txt",2)

