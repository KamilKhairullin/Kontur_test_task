import load.data_loader as dl
import train.trainer as tr
import evaluate.evaluator as ev
import nltk 

tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist  = dl.load_data('train.txt')
uniDist, backwardBiDist, forwardBiDist, trigramDist, wordCasingLookup = tr.train(tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)

testSentences = [
"ЗАО ПРЕДПРИЯТИЕ ПОЖАРНОЙ БЕЗОПАСНОСТИ 'ПОЖКОМПЛЕКТ-1'"
]


for sentence in testSentences:
    tokensCorrect = nltk.word_tokenize(sentence)
    tokens = [token.lower() for token in tokensCorrect]
    tokensTrueCase = ev.getTrueCase(tokens, 'title', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
    print(" ".join(tokensTrueCase))