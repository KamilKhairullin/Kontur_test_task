import string
import math
import pickle
import nltk

class Truecaser():

    def __init__(self):
        self.__tokens = []
        self.__unigram = nltk.FreqDist()
        self.__back_bigram = nltk.FreqDist() 
        self.__forward_bigram = nltk.FreqDist() 
        self.__trigram = nltk.FreqDist() 
        self.__casing_vocabulary = dict()

    def fit(self, path_to_txt, limit):
        i = limit
        sentences = []
        for sentence in open(path_to_txt, encoding='utf-8'):
            sentences.append(sentence.strip('\n'))
            i = i  - 1
            if i == 0:
                break
        tokens = [sentence.split(" ") for sentence in sentences]
        for token in tokens:
          if not token[0].isupper():
              if token[0] not in string.punctuation: 
                  token[0] = token[0][0].lower() + token[0][1:]
              elif len(token[0]) > 2:
                  token[0] = token[0][0] + token[0][1].lower() + token[0][1:]
            
        self.tokens = tokens
        return tokens

    def train(self):
        for token in self.tokens:
            self.__create_unigram(token)
            self.__create_forward_bigram(token)
            self.__create_back_bigram(token)
            self.__create_trigram(token)

    def predict(self, sentence):
        sentenceTrueCase = []
        for i in range(0, len(sentence)):
            word = sentence[i]
            if word in string.punctuation or word.isdigit():
                sentenceTrueCase.append(word)
            elif word in self.casing_vocabulary:
                if len(self.casing_vocabulary[word]) == 1:
                    sentenceTrueCase.append(list(self.casing_vocabulary[word])[0])
                else:
                    previous_word = sentence[i - 1] if i > 0  else None
                    next_word = sentence[i + 1] if (i < len(sentence) - 1) else None
                    best_word = self.__get_best_word(word, previous_word, next_word)
                    sentenceTrueCase.append(best_word)
                if i == 0:
                    if sentenceTrueCase[0] not in string.punctuation: 
                        sentenceTrueCase[0] = sentenceTrueCase[0][0].upper() + sentenceTrueCase[0][1:]
                    else:
                        sentenceTrueCase[0] = sentenceTrueCase[0][0] + sentenceTrueCase[0][1].upper() + sentenceTrueCase[0][1:]
            else:
                sentenceTrueCase.append(word.title())
        return sentenceTrueCase
    
    def save_model(self, name):
        f = open(name, 'wb')
        pickle.dump(self.unigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.back_bigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.forward_bigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.trigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.casing_vocabulary, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def load_model(self, path):
        f = open(path, 'rb')
        self.unigram = pickle.load(f)
        self.back_bigram = pickle.load(f)
        self.forward_bigram = pickle.load(f)
        self.trigram = pickle.load(f)
        self.casing_vocabulary = pickle.load(f)
        f.close()

    def __get_best_word(self, word, previous_word, next_word):
        predicted_word = None
        highest_score = float("-inf")

        for possible_word in self.casing_vocabulary[word]:
            score = self.__get_score(possible_word, previous_word, next_word)
            if score > highest_score:
                predicted_word = possible_word
                highest_score = score
        return predicted_word

    def __get_score(self, word, previous_word, next_word):
        k = 5.0
        unigram_score = self.__get_unigram_score(word, k)
        back_bigram_score = self.__get_back_bigram_score(word, previous_word, k)
        forward_bigram_score = self.__get_forward_bigram_score(word, next_word, k)
        trigram_score = self.__get_trigram_score(word, previous_word, next_word, k)
        score = math.log(unigram_score) + math.log(back_bigram_score) + math.log(forward_bigram_score) + math.log(trigram_score)
        return score

    def __get_unigram_score(self, word, coefficient):
        divisor = self.unigram[word] + coefficient
        denominator = 0
        for case in self.casing_vocabulary[word.lower()]:
            denominator += self.unigram[case] + coefficient
        return divisor / denominator

    def __get_back_bigram_score(self, word, previous_word, coefficient):
        if previous_word != None:  
            divisor = self.back_bigram[previous_word + '_' + word] + coefficient
            denominator = 0    
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.back_bigram[previous_word + '_'+ word] + coefficient
            return divisor / denominator
        else:
            return 1

    def __get_forward_bigram_score(self, word, next_word, coefficient):
        if next_word != None:  
            divisor = self.forward_bigram[word + '_' + next_word] + coefficient
            denominator = 0    
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.forward_bigram[word + '_'+ next_word] + coefficient
            return divisor / denominator
        else:
            return 1

    def __get_trigram_score(self, word, previous_word, next_word, coefficient):
        if previous_word != None and next_word != None:
            divisor = self.trigram[previous_word + "_" + word + "_" + next_word] + coefficient
            denominator = 0    
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.trigram[previous_word + "_" + word + "_" + next_word] + coefficient
            return divisor / denominator
        else:
            return 1

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
                biword = previous_word + "_" + word
                self.back_bigram[biword] += 1
            
    def __create_forward_bigram(self, sentence):
        for i in range(0, len(sentence) - 1):
            word = sentence[i]

            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                biword = word + "_" + next_word
                self.forward_bigram[biword] += 1
    
    def __create_trigram(self, sentence):
        for i in range(1, len(sentence) - 1):
            word = sentence[i]

            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                previous_word = sentence[i - 1]
                triword = previous_word + "_" + word + "_" + next_word
                self.trigram[triword] += 1

    def __add_to_casing_vocabulary(self, word):
        if word.lower() not in self.casing_vocabulary:
            self.casing_vocabulary[word.lower()] = set()

        temp = self.casing_vocabulary[word.lower()]
        temp.add(word)
        self.casing_vocabulary[word.lower()] = temp
