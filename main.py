import nltk
import models.truecaser as tc
import tests.F1_score_evaluator as ev
import string

def join_punctuation(seq):
    characters = {'(', ')', '.', ','}
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current

model = tc.Truecaser()
#tokens = model.fit('train.txt', 100)
#model.train()
#model.save_model('model.obj')
model.load_model('model.obj')


tokens = []
c = 20000

#clear predict file 
file = open('tests/test_2.txt', 'w')
file.close()


predict_file = open('tests/test_2.txt', "a", encoding='utf-8')

answer = ""
for sentence in open('tests/test_1.txt', encoding='utf-8'):
    tokens = nltk.word_tokenize(sentence)
    tokens_lower = [token.lower() for token in tokens]
    x = model.predict(tokens_lower)

    x = list(join_punctuation(x))
    x = " ".join(x)
    x = x.replace("`` ", '"')
    x = x.replace(" ''", '"')
    """
    x = x.replace("( ", "(")
    x = x.replace(" )", ")")
    x = x.replace(" .", ".")
    x = x.replace(" ,", ",")
    if x[0] == '"':
        x = x.replace('" ', '"')
    """
    answer = answer + x + '\n'


    c = c  - 1
    if c == 0:
        c = 20000
        print('start writing to file..')
        predict_file.write(answer)
        answer = ""
        print('ended writing to file .. ')

predict_file.write(answer)
predict_file.close()
eval = ev.F1Evaluator('tests/test_1.txt', 'tests/test_2.txt')
eval.evaluate()
