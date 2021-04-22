import nltk

def load_data(path_to_txt):
    uniDist = nltk.FreqDist()
    backwardBiDist = nltk.FreqDist() 
    forwardBiDist = nltk.FreqDist() 
    trigramDist = nltk.FreqDist() 
    wordCasingLookup = {}

    i = 5000
    sentences = []
    for line in open(path_to_txt, encoding='utf-8'):
        i = i  - 1
        sentences.append(line.strip())
        if i == 0:
            break
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    return (tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
