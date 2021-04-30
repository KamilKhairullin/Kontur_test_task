import nltk
import models.truecaser as tc
import tests.tester as tester
import string


test_path = 'tests/test_1.txt'
pred_path = 'tests/test_2.txt'

model = tc.Truecaser()
model.load_model('model.obj')
#tokens = model.fit('/content/drive/MyDrive/train.txt')
#model.train()
#model.save_model('model.obj')

#clear predict file 
file = open(pred_path, 'w')
file.close()

buffer = 20000
counter = 0
block = 0
answer = ""
for sentence in open(test_path, encoding='utf-8'):
    sentence = sentence.strip('\n')
    tokens = sentence.split(" ")
    tokens_lower = [token.lower() for token in tokens]
    x = model.predict(tokens_lower)

    x = " ".join(x)
    answer = answer + x + '\n'
    counter = counter  + 1
    if counter == buffer:
        counter = 0
        block += 1
        print('start writing to file.. Block [' + str(block) + "] of size " + str(buffer) + " lines")
        predict_file = open(pred_path, "a", encoding='utf-8')
        predict_file.write(answer)
        predict_file.close()
        print('ended writing to file .. ')
        answer = ""
   
predict_file = open(pred_path, "a", encoding='utf-8')
predict_file.write(answer)
predict_file.close()
print('Ended.')

eval = tester.Tester(test_path, pred_path)
eval.evaluate_F1()
eval.evaulate_consistency()

