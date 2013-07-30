def splitData(data, M, k, seed):
    """Split data into test and train set randomly
    """
    test = []
    train = []
    random.seed(seed)
    
    for user, item in data:
        if random.randint(0, M) == k:
            test.append([user, item])
        else:
            train.append([user, item])
    return train, test
    
def recall(train, test, N):
    """Calculate recall
    """
    hit = 0
    all = 0
    
    for user in train.keys():
        tUser = test[user]
        rank = getRecommendation(user, N)
        for item, puItem in rank:
            if item in tUser:
                hit += 1
        all += len(tUser)
    return  hit / (all * 1.0)

def precision(train, test, N):
    """Calculate precision
    """
    hit = 0
    all = 0
    
    for user in train.keys():
        tUser = test[user]
        rank = getRecommendation(user, N)
        for item, puItem in rank:
            if item in tUser:
                hit += 1
        all += N
    return hit / (all * 1.0)

def coverage(train, test, N):
    """Calculate coverage
    """
    recommendItems = set()
    allItems = set()
    
    for user in train.keys():
        allItems.add(item)
    rank = getRecommendation(user, N)
    for item, puItem in rank:
        recommendItems.add(item)
    return len(recommendItems) / (len(allItems) * 1.0)
    
def popularity(train, test, N):
    """Calculate popularity
    """
    itemPopularity = dict()
    
    for user, item in train.keys():
        if item not in itemPopularity:
            itemPopularity[item] = 0
        itemPopularity[item] += 1
    
    ret = 0
    n = 0
    
    for user in train.keys():
        rank = getRecommendation(user, N)
        for item, puItem in rank:
            ret += math.log(1 + itemPopularity[item])
            n += 1
    ret /= n * 1.0
    return ret