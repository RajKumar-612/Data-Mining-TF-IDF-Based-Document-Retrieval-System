import os
import math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpusroot = "./US_Inaugural_Addresses"


def getTokens(qstring):
    tokenizer = RegexpTokenizer(r"[a-zA-Z]+")
    tokens = tokenizer.tokenize(qstring)
    stop_words = sorted(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


df = {}
tf = {}
N = 0


def idf(token):
    if token in df:
        return math.log(N / df[token], 10)
    return -1


def getidf(token):
    stemmer = PorterStemmer()
    return idf(stemmer.stem(token.lower()))


def gettf(filename, token):
    if filename not in tf or token not in tf[filename]:
        return 0
    else:
        return 1 + math.log(tf[filename][token], 10)


def gettf_idf(filename, token):
    return gettf(filename, token) * idf(token)


def getweight(filename, token):
    token = token.lower()
    stemmer = PorterStemmer()
    token = stemmer.stem(token)
    doc_weights = norm_tfidf(filename)
    if token in doc_weights:
        return doc_weights[token]
    return 0


def norm_tfidf(filename):
    doc_weights = {}
    sum = 0
    for token in tf[filename].keys():
        wtfidf = gettf_idf(filename, token)
        sum = sum + wtfidf**2
        doc_weights[token] = wtfidf
    sum = math.sqrt(sum)
    for token in tf[filename].keys():
        doc_weights[token] = doc_weights[token] / sum
    return doc_weights


def query_norm(tokens):
    sum = 0
    query_weights = {}
    for token in tokens:
        wtfidf = 1 + math.log(tokens.count(token))
        sum = sum + wtfidf**2
        query_weights[token] = wtfidf
    sum = math.sqrt(sum)
    for token in tokens:
        query_weights[token] = wtfidf / sum
    return query_weights


def query(qstring):
    tokens = getTokens(qstring.lower())
    query_weights = query_norm(tokens)
    cosine_sim = 0
    file = None
    for filename in os.listdir(corpusroot):
        if filename.startswith("0") or filename.startswith("1"):
            doc_weights = norm_tfidf(filename)
            sum = 0
            for token in tokens:
                if token in doc_weights:
                    sum += query_weights[token] * doc_weights[token]
            cosine_sim = max(cosine_sim, sum)
            if cosine_sim == sum:
                file = filename
    return (file, cosine_sim)


for filename in os.listdir(corpusroot):
    if filename.startswith("0") or filename.startswith("1"):
        file = open(os.path.join(corpusroot, filename), "r", encoding="windows-1252")
        N = N + 1
        tokens = getTokens(file.read().lower())
        file.close()
        tf[filename] = {}
        for token in tokens:
            if token in tf[filename].keys():
                tf[filename][token] += 1
            else:
                tf[filename][token] = 1
        for token in tf[filename].keys():
            if token not in df:
                df[token] = 1
            else:
                df[token] += 1

print("%.12f" % getidf("british"))
print("%.12f" % getidf("union"))
print("%.12f" % getidf("war"))
print("%.12f" % getidf("military"))
print("%.12f" % getidf("great"))
print("--------------")
print("%.12f" % getweight("02_washington_1793.txt", "arrive"))
print("%.12f" % getweight("07_madison_1813.txt", "war"))
print("%.12f" % getweight("12_jackson_1833.txt", "union"))
print("%.12f" % getweight("09_monroe_1821.txt", "british"))
print("%.12f" % getweight("05_jefferson_1805.txt", "public"))
print("--------------")
print("(%s, %.12f)" % query("pleasing people"))
print("(%s, %.12f)" % query("british war"))
print("(%s, %.12f)" % query("false public"))
print("(%s, %.12f)" % query("people institutions"))
print("(%s, %.12f)" % query("violated willingly"))
