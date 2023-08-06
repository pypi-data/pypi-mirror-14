import os
import sys
from collections import defaultdict
from . import helpers as util
import requests
import json

class Empath:
    def __init__(self, backend_url="http://54.148.189.209:8000"):
        self.cats = defaultdict(list)
        self.staging = {}
        self.backend_url = backend_url
        self.base_dir = os.path.dirname(util.__file__)
        self.load(self.base_dir+"/data/categories.tsv")
        for f in os.listdir(self.base_dir+"/data/user/"):
            if len(f.split(".")) > 1 and f.split(".")[1] == "empath":
                print("loading ",f)
                self.load(self.base_dir+"/data/user/"+f)

    def load(self,file):
        with open(file,"r") as f:
            for line in f:
                cols = line.strip().split("\t")
                name = cols[0]
                terms = cols[1:]
                for t in set(terms):
                    self.cats[name].append(t)
                    #self.invcats[t].append(name)

    def analyze(self,doc,cats=None,tokenizer="default",normalize=True):
        if tokenizer == "default":
            tokenizer = util.default_tokenizer
        elif tokenizer == "bigrams":
            tokenizer = util.bigram_tokenizer
        if not hasattr(tokenizer,"__call__"):
            raise Exception("invalid tokenizer")
        if not cats:
            cats = self.cats.keys()
        invcats = defaultdict(list)
        for k in cats:
           for t in self.cats[k]: invcats[t].append(k)
        count = {}
        tokens = 0.0
        for cat in cats: count[cat] = 0.0
        for tk in tokenizer(doc):
            tokens += 1.0
            for cat in invcats[tk]:
                count[cat]+=1.0
        if normalize:
            for cat in count.keys():
                count[cat] = count[cat] / tokens
        return count

    def create_category(self,name,seeds,size=100):
        resp = requests.post(self.backend_url + "/create_category", json={"terms":seeds,"size":size})
        print(resp.text)
        results = json.loads(resp.text)
        self.cats[name] = list(set(results))
        with open(self.base_dir+"/data/user/"+name+".empath","w") as f:
            f.write("\t".join([name]+results))
