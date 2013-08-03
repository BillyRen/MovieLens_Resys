# -*- coding: utf-8 -*-
import math
import random

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
        for item in train[user].keys():
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
    
def userSimilarity(train):
    """Calculate user similarity
    """
    W = {}
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue 
            W[u][v] = len(train[u] & train[v])
            W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
    return W
    
def userSimilarityInverse(train):
    """Calculate user similarity using inverse table
    """
    itemUsers = {}
    for u, item in train.items():
        for i in item.keys():
            if i not in itemUsers:
                itemUsers[i] = set()
            itemUsers[i].add(u)
            
    C = {}
    N = {}
    for i, users in itemUsers.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue 
                C[u][v] += 1
                
    W = {}
    for u, relatedUsers in C.items():
        for v, cUV in relatedUsers.items():
            W[u][v] = cUV / math.sqrt(N[u] * N[v])
    return W
    
def userSimilarityIIF(train):
    itemUsers = {}
    for u, item in train.items():
        for i in item.keys():
            if i not in itemUsers:
                itemUsers[i] = set()
            itemUsers[i].add(u)
            
    C = {}
    N = {}
    for i, users in itemUsers.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue 
                C[u][v] += 1 / math.log(1 + len(users))
    
    W = {}
    for u, relatedUsers in C.items():
        for v, cUV in relatedUsers.items():
            W[u][v] = cUV / math.sqrt(N[u] * N[v])
    return W              
        
    
def recommendationUser(user, train, W, K):
    """userCF
    """
    rank = {}
    interactedItems = train[user]
    for v, wUV in sorted(W[user].items, key = itemgetter(1), reverse = True)[0:K]:
        for i, rUV in train[v].items:
            if i in interactedItems:
                continue 
            rank[i] += wUV * rUV
    return rank
    
def itemSimilarity(train):
    C = {}
    N = {}
    for user, item in train.items():
        for i in user:
            N[i] += 1
            for j in user:
                if i == j:
                    continue 
                C[i][j] += 1
                
    W = {}
    for i, relatedItems in C.items():
        for j, cIJ in relatedItems.items():
            W[i][j] = cIJ / math.sqrt(N[i] * N[j])
    return W
    
"""下一步要完成的：itemCF的推荐函数
"""