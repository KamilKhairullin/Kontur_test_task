import nltk
import models.truecaser as tc

model = tc.Truecaser()
#tokens = model.fit('train.txt', 100)
#model.train()
#model.save_model('model.obj')
model.load_model('model.obj')
testSentences = [
'ЗАО "Учебный центр ФОРС"',
'Государственное предприятие "Клен"',
'Общество с ограниченной ответственностью "САКСЭССФУЛ КЭТ"'
]

tokens = []
c = 2
for sentence in open('test.txt', encoding='utf-8'):
    tokens = nltk.word_tokenize(sentence)
    tokens_lower = [token.lower() for token in tokens]
    x = model.predict(tokens_lower)
    x = " ".join(x)
    x = x.replace("`` ", '"')
    x = x.replace(" ''", '"')
    print(x)
    c = c  - 1
    if c == 0:
        break