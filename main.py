import nltk
import models.truecaser as tc

model = tc.Truecaser()
tokens = model.fit('train.txt', 1000000)
model.train()

testSentences = [
'АДЫГЕЙСКАЯ РЕСПУБЛИКАНСКАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ СОЮЗА РОССИЙСКИХ ПИСАТЕЛЕЙ',
'АДЫГЕЙСКАЯ ГОРОДСКАЯ ОРГАНИЗАЦИЯ ОБЩЕРОССИЙСКОЙ ОБЩЕСТВЕННОЙ ОРГАНИЗАЦИИ "РОССИЙСКАЯ ОБОРОННАЯ СПОРТИВНО-ТЕХНИЧЕСКАЯ ОРГАНИЗАЦИЯ-РОСТО (ДОСААФ)"',
'ИУДЕЙСКАЯ МЕСТНАЯ РЕЛИГИОЗНАЯ ОРГАНИЗАЦИЯ "МАЙКОПСКАЯ ЕВРЕЙСКАЯ ОБЩИНА"',
'АРОО ТАТАРСКОЕ КУЛЬТУРНО-ПРОСВЕТИТЕЛЬСКОЕ ОБЩЕСТВО "ДУСЛЫК" (ДРУЖБА)',
'ДОШКОЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ДЕТСКИЙ САД ОБЩЕОБРАЗОВАТЕЛЬНОГО ВИДА №14 "РЯБИНУЩКА"'
]

tokens = []
for sentence in testSentences:
    tokensCorrect = nltk.word_tokenize(sentence)
    tokens = [token.lower() for token in tokensCorrect]
    x = model.predict(tokens)
    print(" ".join(x))
