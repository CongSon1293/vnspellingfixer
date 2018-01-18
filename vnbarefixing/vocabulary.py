import cPickle as pickle
class Vocabulary:
    def __init__(self):
        self.token_2_id = dict()
        self.id_2_token = dict()
        self.doc_freq = dict()
        self.term_freq = dict()
        self.n_docs = 0

    def get_token_id(self,token,updating=True):

        token_id = -1
        if len(token) < 1:
            return token_id
        try:
            token_id = self.token_2_id[token]
        except:
            if updating:
                token_id = len(self.token_2_id)
                self.token_2_id[token] = token_id
                self.id_2_token[token_id] = token
                self.doc_freq[token_id] = 0
                self.term_freq[token_id] = 0

        return token_id

    def get_sentence_token_ids(self,sentence,updating=True):
        tokens = sentence.split(" ")
        token_ids = []
        distinct_token_ids = set()
        for token in tokens:
            token_id = self.get_token_id(token,updating)
            if token_id != -1:
                token_ids.append(token_id)
                if updating:
                    self.term_freq[token_id] += 1
                    distinct_token_ids.add(token_id)
        if updating:
            for token_id in distinct_token_ids:
                self.doc_freq[token_id] += 1
            self.n_docs += 1
        return token_ids

    def save(self,path):
        pickle.dump(self,open(path,"wb"))

    @staticmethod
    def load(path):
        return pickle.load(open(path,"rb"))







