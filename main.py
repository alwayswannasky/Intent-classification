from flask import Flask, request, jsonify
import numpy as np
import spacy
import pickle

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def encode_sentences(sentences):
    n_sentences = len(sentences)
    X = np.zeros((n_sentences, nlp.vocab.vectors_length))

    for idx, sentence in enumerate(sentences):
        doc = nlp(sentence)
        X[idx, :] = doc.vector
    return X


@app.route('/', methods=['GET'])
def hello():
    return 'Hello'


@app.route('/bot', methods=['POST'])
def model_intent():
    sentence = request.json['sentence'].lower()
    print(sentence)
    v = encode_sentences([sentence])
    list_of_prob = model.predict_proba(v).tolist()[0]
    list_of_prob.sort(reverse=True)
    top_3_index = list_of_prob[:3]
    top_3_scores = [model.predict_proba(v).tolist()[0].index(i) for i in top_3_index]
    array_of_intents = [(intents[top_3_scores].tolist()[i], top_3_index[i]) for i in range(3)]
    print(array_of_intents)
    return jsonify({'info': array_of_intents})


if __name__ == '__main__':
    filename = 'SVC.sav'
    model = pickle.load(open(filename, 'rb'))
    nlp = spacy.load('ru_core_news_lg')

    intents = list()
    with open('intents.txt', 'r') as file:
        for line in file:
            intents.append(line[:-1])
    intents = np.asarray(intents)

    app.run(host='0.0.0.0', port=8080, debug=True)
