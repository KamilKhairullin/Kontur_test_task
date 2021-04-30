import nltk
import models.truecaser as tc
import tests.F1_score_evaluator as ev
import string

def join_punctuation(seq):
    characters = {'(', ')', '.', ',', '``', "''"}
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current

test_path = '/content/drive/MyDrive/test_1.txt'
pred_path = '/content/drive/MyDrive/test_2.txt'

model = Truecaser()
#tokens = model.fit('/content/drive/MyDrive/train.txt', 1000000000)
#model.train()
#model.save_model('model.obj')
model.load_model('/content/model.obj')


tokens = []
c = 100000
stopper = 100

#clear predict file 
file = open(pred_path, 'w')
file.close()



answer = ""
for sentence in open(test_path, encoding='utf-8'):
    #tokens = nltk.word_tokenize(sentence)
    sentence = sentence.strip('\n')
    tokens = sentence.split(" ")
    #print(tokens)
    tokens_lower = [token.lower() for token in tokens]
    x = model.predict(tokens_lower)

    #x = list(join_punctuation(x))
    x = " ".join(x)

    #x = x.replace("``", '"')
    #x = x.replace("''", '"')

    answer = answer + x + '\n'


    c = c  - 1
    if c == 0:
        c = 50000
        print('start writing to file..')
        predict_file = open(pred_path, "a", encoding='utf-8')
        predict_file.write(answer)
        predict_file.close()
        answer = ""
        print('ended writing to file .. ')
        stopper -= 1
        if stopper == 0:
          break
   
predict_file = open(pred_path, "a", encoding='utf-8')
predict_file.write(answer)
predict_file.close()

eval = F1Evaluator(test_path, pred_path)
eval.evaluate()
