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

    allFreqItemSets = []

    frequen1Items = filterItemSetByMinSupport(frequentKItems, relativeMinSupport)

    allFreqItemSets.extend(frequen1Items)

    kItemSets = getKEquals1combinations(frequen1Items)

    k=2
    while True:
        kFreqItemSets = getTrxHavingkItemSets(kItemSets,relativeMinSupport,transactions)

        if len(kFreqItemSets) == 0:
            break
        else:
            allFreqItemSets.extend(kFreqItemSets)

        print "Freq k= ",k,"->",kFreqItemSets

        kItemSets = getNextItemCombinations(frequen1Items,kFreqItemSets)

        k = k + 1

    print allFreqItemSets

def getNextItemCombinations(frequen1Items, kFreqItemSets):

    permutaitonsAll = []
    for itemSetToCombine in kFreqItemSets:
        permuationGo = []
        toCombine = itemSetToCombine.itemSet
        for oneItem in frequen1Items:
            if not oneItem in toCombine:
                permuationGo = toCombine[:]
                permuationGo.append(oneItem)
                permutaitonsAll.append(permuationGo)

    return permutaitonsAll



def filterItemSetByMinSupport(frequentKItems, relativeMinSupport):
    #   Remove k=1 without min support
    for category in frequentKItems.keys():
        support = frequentKItems[category]
        if support <= relativeMinSupport:
            frequentKItems.pop(category, None)
    print frequentKItems
    # printFrequentItems(frequentKItems,"frequent1Items.txt")
    frequenKItems = []
    for aFreq1Itemcategory in frequentKItems.keys():
        frequenKItems.append(aFreq1Itemcategory)
    return frequenKItems


def getTrxHavingkItemSets(kItemSets,relativeMinSupport,transactions):
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

        itemSetCll = ItemSet(aItemSet)
        kItemSetToSupport[itemSetCll] = support

    return filterItemSetByMinSupport(kItemSetToSupport,relativeMinSupport)


class ItemSet:
    def __init__(self, itemSet):
        self.itemSet = itemSet

    def __repr__(self):
        return str(self.itemSet)


def getKEquals1combinations(frequen1Items):
    k=2
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

