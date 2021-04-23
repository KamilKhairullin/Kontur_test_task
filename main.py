import nltk
import models.truecaser as tc

model = tc.Truecaser()
tokens = model.fit('train.txt', 30000)
model.train()

testSentences = [
'ГОСУДАРСТВЕННОЕ УЧРЕЖДЕНИЕ "ГОСУДАРСТВЕННАЯ СЕМЕННАЯ ИНСПЕКЦИЯ" АЗНАКАЕВСКОГО РАЙОНА',
'ГОССЕМИНСПЕКЦИЯ АЗНАКАЕВСКОГО РАЙОНА',
'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "АЗНАКАЙ КИЕМНЭРЕ"'
]

tokens = []
for sentence in testSentences:
    tokensCorrect = nltk.word_tokenize(sentence)
    tokens = [token.lower() for token in tokensCorrect]
    x = model.predict(tokens)
    print(" ".join(x))
