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
        self.__casing_vocabulary = dict() #maps word in lower case to all it's casing variations (String : set{String})

    """ fit()
    This is where the data is preprocessed: 
    for each sentence separated by the "end of line" character, the "end of line" character is removed 
    and the sentence is split into separate tokens.

    Parameters:
    path_to_txt (String) : path to train data

    Returns:
    [[String]] : Tokens 

   """
    def fit(self, path_to_txt):
        sentences = []
        for sentence in open(path_to_txt, encoding='utf-8'):
            sentences.append(sentence.strip('\n'))
        
        # Split sentences into tokens by 'space' divisor
        tokens = [sentence.split(" ") for sentence in sentences]

        # Preprocessing of first word. If it not uppercase, make it's first letter lowercase.
        # If first letter is punctuation - make second letter lowercase instead.
        for token in tokens:
          if not token[0].isupper():
              if token[0] not in string.punctuation: 
                  token[0] = token[0][0].lower() + token[0][1:]
              elif len(token[0]) > 2:
                  token[0] = token[0][0] + token[0][1].lower() + token[0][1:]
            
        self.tokens = tokens
        return tokens
    
    """ train()
    This is where unigram, forward_bigram, back_bigram, trigram 
    are created based on the data processed by the fit method.

    Parameters:
    None

    Returns:
    Void
    """
    def train(self):
        for token in self.tokens:
            self.__create_unigram(token)
            self.__create_forward_bigram(token)
            self.__create_back_bigram(token)
            self.__create_trigram(token)

    """ predict()
    Predicts casing of given sentence

    Parameters:
    [String] : sentence

    Returns:
    [String] : sentenceTrueCase
    """
    def predict(self, sentence):
        sentenceTrueCase = []
        #for each word in sentence
        for i in range(0, len(sentence)):
            word = sentence[i]
            #if word is punctuation or digit just add it.
            if word in string.punctuation or word.isdigit():
                sentenceTrueCase.append(word)
            #if word in our vocabulary
            elif word in self.casing_vocabulary:
                # if vocabulary have only one version of word casing
                if len(self.casing_vocabulary[word]) == 1:
                    sentenceTrueCase.append(list(self.casing_vocabulary[word])[0])
                # if vocabulary have multiple varsions of casing
                else:
                    #get previous word
                    previous_word = sentence[i - 1] if i > 0  else None
                    #get next word
                    next_word = sentence[i + 1] if (i < len(sentence) - 1) else None
                    #find and append best casing
                    best_word = self.__get_best_word(word, previous_word, next_word)
                    sentenceTrueCase.append(best_word)
                #If this is a first word in sentence, make it's first character upper case.
                if i == 0:
                    if sentenceTrueCase[0] not in string.punctuation: 
                        sentenceTrueCase[0] = sentenceTrueCase[0][0].upper() + sentenceTrueCase[0][1:]
                    else:
                        sentenceTrueCase[0] = sentenceTrueCase[0][0] + sentenceTrueCase[0][1].upper() + sentenceTrueCase[0][1:]
            # If word not in vocabulary, just return template answer
            else:
                sentenceTrueCase.append(word.title())
        return sentenceTrueCase

    """ save_model()
    saves self.__unigram, self.__back_bigram, self.__forward_bigram, self.__trigram, self.casing_vocabulary
    to .obj file using pickle.

    Parameters:
    None

    Returns:
    Void
    """
    def save_model(self, name):
        f = open(name, 'wb')
        pickle.dump(self.unigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.back_bigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.forward_bigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.trigram, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.casing_vocabulary, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    """ load_model()
    loads self.__unigram, self.__back_bigram, self.__forward_bigram, self.__trigram, self.casing_vocabulary
    from .obj file using pickle.

    Parameters:
    None

    Returns:
    Void
    """
    def load_model(self, path):
        f = open(path, 'rb')
        self.unigram = pickle.load(f)
        self.back_bigram = pickle.load(f)
        self.forward_bigram = pickle.load(f)
        self.trigram = pickle.load(f)
        self.casing_vocabulary = pickle.load(f)
        f.close()

    """ private get_best_word()
    Evaluates most probable word casing given word in lower case.

    Parameters:
    String : word 
    String : previous_word
    String : next_word

    Returns:
    String : predicted_word
    """
    def __get_best_word(self, word, previous_word, next_word):
        predicted_word = None
        highest_score = float("-inf")

        # Check all possible variations of word.
        for possible_word in self.casing_vocabulary[word]:
            #evaluate score for each possible word
            score = self.__get_score(possible_word, previous_word, next_word)
            if score > highest_score:
                predicted_word = possible_word
                highest_score = score

        #return word with highest score
        return predicted_word

    """ private get_score()
    Evaluates most probable word casing given word in lower case.

    Parameters:
    String : word 
    String : previous_word
    String : next_word

    Returns:
    Float : score
    """

    def __get_score(self, word, previous_word, next_word):
        # We can define weight of any *gram. But in this case they are the same. 
        weight = 5.0
        unigram_score = self.__get_unigram_score(word, weight)
        back_bigram_score = self.__get_back_bigram_score(word, previous_word, weight)
        forward_bigram_score = self.__get_forward_bigram_score(word, next_word, weight)
        trigram_score = self.__get_trigram_score(word, previous_word, next_word, weight)
        #total score calculated as multiplication of logarithms of *gram scores.
        score = math.log(unigram_score) + math.log(back_bigram_score) + math.log(forward_bigram_score) + math.log(trigram_score)
        return score

    """ private get_unigram_score()
    Evaluates most probable word casing given word in lower case.

    Parameters:
    String : word 
    Float : coefficient (weight)

    Returns:
    Float : score
    """
    def __get_unigram_score(self, word, coefficient):
        # unigram frequency of given casing
        divisor = self.unigram[word] + coefficient
        denominator = 0
        # unigram frequency of sum of all casings
        for case in self.casing_vocabulary[word.lower()]:
            denominator += self.unigram[case] + coefficient
        #probability of given word is ratio of frequency of given casing and frequensies of all casing.
        return divisor / denominator


    """ private get_back_bigram_score()
    Evaluates most probable word casing given word in lower case and previous word in lower case.

    Parameters:
    String : word 
    String : previous_word
    Float : coefficient (weight)

    Returns:
    Float : score
    """
    def __get_back_bigram_score(self, word, previous_word, coefficient):
        if previous_word != None:  
             # bigram frequency of given casing
            divisor = self.back_bigram[previous_word + '_' + word] + coefficient
            denominator = 0    
             # bigram frequency of sum of all casings
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.back_bigram[previous_word + '_'+ word] + coefficient
            #probability of given word is ratio of frequency of given casing and frequensies of all casing
            return divisor / denominator
        #if there is no previous word
        else:
            return 1

    """ private get_forward_bigram_score()
    Evaluates most probable word casing given word in lower case and next word in lower case.

    Parameters:
    String : word 
    String : previous_word
    Float : coefficient (weight)

    Returns:
    Float : score
    """

    def __get_forward_bigram_score(self, word, next_word, coefficient):
        if next_word != None:  
            # bigram frequency of given casing
            divisor = self.forward_bigram[word + '_' + next_word] + coefficient
            denominator = 0    
            # bigram frequency of sum of all casings
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.forward_bigram[word + '_'+ next_word] + coefficient
            #probability of given word is ratio of frequency of given casing and frequensies of all casing
            return divisor / denominator
        #if there is no next word
        else:
            return 1

    """ private get_trigram_score()
    Evaluates most probable word casing given word in lower case and next and previous words in lower case.

    Parameters:
    String : word 
    String : previous_word
    String : next_word
    Float : coefficient (weight)

    Returns:
    Float : score
    """

    def __get_trigram_score(self, word, previous_word, next_word, coefficient):
        if previous_word != None and next_word != None:
            # trigram frequency of given casing
            divisor = self.trigram[previous_word + "_" + word + "_" + next_word] + coefficient
            denominator = 0    
            # trigram frequency of sum of all casings
            for case in self.casing_vocabulary[word.lower()]:
                denominator += self.trigram[previous_word + "_" + word + "_" + next_word] + coefficient
            #probability of given word is ratio of frequency of given casing and frequensies of all casing
            return divisor / denominator
        #if there is no previous or next word
        else:
            return 1

    """ private create_unigram()
    For each word in sentence, adds count assosiated with this word to
    unigram frequency distribution and add this word to casing vocabulary.

    Parameters:
    [String] : sentence

    Returns:
    Void
    """

    def __create_unigram(self, sentence):
        for i in range(0, len(sentence)):
            word = sentence[i]
            self.unigram[word] += 1
            self.__add_to_casing_vocabulary(word)

    """ private create_back_bigram()
    For each word in sentence which have neighbor to the left, adds count assosiated
   with 'previousWord_thisWord' to back_bigram distribution.

    Parameters:
    [String] : sentence

    Returns:
    Void
    """
    def __create_back_bigram(self, sentence):
        #starts with second word
        for i in range(1, len(sentence)):
            word = sentence[i]
            #adds only if there are multiple variations of this word.
            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                previous_word = sentence[i - 1]
                biword = previous_word + "_" + word
                self.back_bigram[biword] += 1
  
    """ private create_forward_bigram()
    For each word in sentence which have neighbor to the right, adds count assosiated
   with 'thisWord_nextWord' to forward_bigram distribution.

    Parameters:
    [String] : sentence

    Returns:
    Void
    """
    def __create_forward_bigram(self, sentence):
        #ends in pre-last word
        for i in range(0, len(sentence) - 1):
            word = sentence[i]
            #adds only if there are multiple variations of this word.
            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                biword = word + "_" + next_word
                self.forward_bigram[biword] += 1

    """ private create_trigram()
    For each word in sentence which have neighbor to the right and left, adds count assosiated
    with 'previousWord_thisWord_nextWord' to trigram distribution.

    Parameters:
    [String] : sentence

    Returns:
    Void
    """
    def __create_trigram(self, sentence):
        #starts with second word, ends with pre-last word
        for i in range(1, len(sentence) - 1):
            word = sentence[i]
            #adds only if there are multiple variations of this word.
            if word.lower() in self.casing_vocabulary and len(self.casing_vocabulary[word.lower()]) > 1:
                next_word = sentence[i + 1]
                previous_word = sentence[i - 1]
                triword = previous_word + "_" + word + "_" + next_word
                self.trigram[triword] += 1


    """ private add_to_casing_vocabulary()
    Adds word to casing_vocabulary

    Parameters:
    String : word

    Returns:
    Void
    """

    def __add_to_casing_vocabulary(self, word):
        # case if word is not in vocab, create set for it.
        if word.lower() not in self.casing_vocabulary:
            self.casing_vocabulary[word.lower()] = set()

        # Add word to vocab.
        temp = self.casing_vocabulary[word.lower()]
        temp.add(word)
        self.casing_vocabulary[word.lower()] = temp