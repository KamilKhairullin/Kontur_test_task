import nltk
import string
import math

class Truecaser():

    def __init__(self):
        self.tokens = []
        self.unigram = nltk.FreqDist()
        self.back_bigram = nltk.FreqDist() 
        self.forward_bigram = nltk.FreqDist() 
        self.trigram = nltk.FreqDist() 
        self.casing_vocabulary = dict()

    def fit(self, path_to_txt, limit):
        i = limit
        sentences = []
        for sentence in open(path_to_txt, encoding='utf-8'):
            sentences.append(sentence.strip('\n'))
            i = i  - 1
            if i == 0:
                break
        tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
        self.tokens = tokens
        return tokens

    def train(self):
        for token in self.tokens:
            self.__create_unigram(token)
            self.__create_forward_bigram(token)
            self.__create_back_bigram(token)
            self.__create_trigram(token)

    def predict(self, tokens):
        for token in tokens:
            print(token)


    def __create_unigram(self, sentence):
        for i in range(0, len(sentence)):
            word = sentence[i]
            self.unigram[word] += 1
            self.__add_to_casing_vocabulary(word)

    def __create_back_bigram(self, sentence):
        for i in range(1, len(sentence)):
            word = sentence[i]
            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                previous_word = sentence[i - 1]
                # ??? make previous word lower case before adding / or make current word -NO ! FIX
                biword = previous_word + "_" + word
                self.back_bigram[biword] += 1
            
    def __create_forward_bigram(self, sentence):
        for i in range(0, len(sentence) - 1):
            word = sentence[i]

            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                # ??? make next word lower case before adding - YES ! FIX
                biword = word + "_" + next_word
                self.forward_bigram[biword] += 1
    
    def __create_trigram(self, sentence):
        for i in range(1, len(sentence) - 1):
            word = sentence[i]

            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                previous_word = sentence[i - 1]
                # ??? make prev high and next lower - YES ! FIX
                triword = previous_word + "_" + word + "_" + next_word
                self.trigram[triword] += 1

    def __add_to_casing_vocabulary(self, word):
        if word.lower() not in self.casing_vocabulary:
            self.casing_vocabulary[word.lower()] = set()

        temp = self.casing_vocabulary[word.lower()]
        temp.add(word)
        self.casing_vocabulary[word.lower()] = temp