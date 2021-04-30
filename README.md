# Тестовое задание. Контур, Data Science 2021.
Камиль Хайруллин (Kamil Khairullin, k.hayrullin@innopolis.university)

## Описание проблемы

Требуется обучить модель, которая сможет приводить символы в наименовании к корректному регистру, так чтобы полученное название наиболее вероятно совпадало с прописанным в уставе ЕГРЮЛ.

## Стратегия решения проблемы

После изучения проблемы я понял, что перед нами стоит задача по определению правильного написания заглавных букв в словах, где такая информация недоступна. Это одна из проблем в NLP, которая называется **Truecasing**. 

Я приступил к изучению данного вопроса, поиску решений и исследований на эту тему. Тогда я наткнулся на исследование [Lucian Vlad Lita, Abe Ittycheriah, Salim Roukos, Nanda Kambhatla (2003). tRuEcasIng](https://www.cs.cmu.edu/~llita/papers/lita.truecasing-acl2003.pdf), которое и взял за основу своего решения. 

В основе решения лежит четыре частотных распределения, в исслледовании называемых:
- **unigram** - для каждого уникального слова, встреченного в training data, хранит количество появлений.
- **forward bigram** - для каждой уникальной пары слов (текущее слово, следующее слово), встреченной в training data, хранит количество появлений.
- **backward bigram** - для каждой уникальной пары слов (предыдущее слово, текущее слово), встреченной в training data, хранит количество появлений.
- **trigram** - для каждой уникальной тройки слов (предыдущее слово, текущее слово, следующее слово), встреченной в training data, хранит количество появлений. \
\
А так же жадный алгоритм, который высчитывает вероятность написания слова на основе четырёх вышеупомянутых структур.

![CodeCogsEqn](https://user-images.githubusercontent.com/54369751/116720543-ff8cfe80-a9e4-11eb-9a05-e8115d5392a8.png)

После чего выдаётся самый вероятный casing. 

<a href="https://www.codecogs.com/eqnedit.php?latex=score(w_0)&space;=&space;P_{unigram}(w_0)&space;*&space;P_{forward&space;bigram}(w_0,&space;w_1)&space;*&space;P_{backward&space;bigram}(w_{-1},&space;w_0)&space;*&space;P_{trigram}(w_{-1},&space;w_0,&space;w_1)" target="_blank"><img src="https://latex.codecogs.com/png.latex?score(w_0)&space;=&space;P_{unigram}(w_0)&space;*&space;P_{forward&space;bigram}(w_0,&space;w_1)&space;*&space;P_{backward&space;bigram}(w_{-1},&space;w_0)&space;*&space;P_{trigram}(w_{-1},&space;w_0,&space;w_1)" title="score(w_0) = P_{unigram}(w_0) * P_{forward bigram}(w_0, w_1) * P_{backward bigram}(w_{-1}, w_0) * P_{trigram}(w_{-1}, w_0, w_1)" /></a>
