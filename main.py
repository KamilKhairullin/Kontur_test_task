import nltk
import models.truecaser as tc

model = tc.Truecaser()
#tokens = model.fit('train2.txt', 3)
#model.train()
testSentences = [
"ЗАО ПРЕДПРИЯТИЕ ПОЖАРНОЙ БЕЗОПАСНОСТИ 'ПОЖКОМПЛЕКТ-1'"
]

tokens = []
for sentence in testSentences:
    tokensCorrect = nltk.word_tokenize(sentence)
    tokens = [token.lower() for token in tokensCorrect]

model.predict(tokens)
