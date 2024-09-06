# -*- coding: utf-8 -*-
"""Word_Embeddings_e_Geração_de_Texto.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rSiAjDOqaJZSOAG4SMtI92ZSOpVr29e-

**ALUNO:** Lucas de Lima da Silva

**MATRÍCULA:** 121110517
"""

!pip install unidecode
from unidecode import unidecode
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models.callbacks import CallbackAny2Vec

import numpy as np
import pandas as pd

import gensim
import re
import string
import nltk
import time

from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

nltk.download('stopwords')

data = pd.read_csv('/content/teor_inteiro_jusbrasil.csv')

data.head()

# Tentei uma versão de pré-processamento com lematização,
# mas acabou por deixar a geração de texto, busca de similaridade e analogias
# com menos sentido

def preprocess_text(text):
    text = unidecode(text).lower()

    text = re.sub(r'\d+', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\W+', ' ', text)

    words = word_tokenize(text)

    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in words if word not in stop_words and len(word) > 2]

    return words

documents = data['text'].astype(str).tolist()
preprocessed_documents = [preprocess_text(doc) for doc in documents]

for i in range(10): print(preprocessed_documents[i])

# TREINAMENTO DO MODELO Skip-Gram

class MonitorCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
        self.start_time = time.time()

    def on_epoch_begin(self, model):
        print(f"Iniciando época {self.epoch + 1}")

    def on_epoch_end(self, model):
        elapsed_time = time.time() - self.start_time
        elapsed_time_minutes = elapsed_time / 60
        avg_time_per_epoch = elapsed_time / (self.epoch + 1)
        estimated_time_remaining = avg_time_per_epoch * (model.epochs - self.epoch - 1)
        estimated_time_remaining_minutes = estimated_time_remaining / 60

        print(f"Época {self.epoch + 1} finalizada. Tempo decorrido: {elapsed_time_minutes:.2f} minutos.")
        print(f"Tempo médio por época: {avg_time_per_epoch / 60:.2f} minutos.")
        print(f"Tempo estimado restante: {estimated_time_remaining_minutes:.2f} minutos.")

        self.epoch += 1

monitor = MonitorCallback()

model1 = Word2Vec(
    preprocessed_documents,
    vector_size=200,
    window=15,
    sg=1,
    workers=6,
    min_alpha=0.0001,
    alpha=0.03,
    callbacks=[monitor],
    epochs=10,
    min_count=3
)

model1.save("jusbrasil2")

# PALAVRAS SIMILARES

print(model1.wv.most_similar('juiz', topn=10))

print(model1.wv.most_similar('crime', topn=10))

print(model1.wv['juiz'])

# ANALOGIAS

# PROMOTORA ESTÁ PARA JUIZ ASSIM COMO PROMOTOR ESTÁ PARA?
print(model1.wv.most_similar(positive=['promotora', 'juiz'], negative=['promotor'], topn=1))

# ACUSADO ESTÁ PARA RÉU ASSIM COMO TESTEMUNHA ESTÁ PARA?
print(model1.wv.most_similar(positive=['acusado', 'reu'], negative=['testemunha'], topn=1))

# DEFENSOR ESTÁ PARA ACUSADO ASSIM COMO ADVOGADO ESTÁ PARA?
print(model1.wv.most_similar(positive=['defensor', 'acusado'], negative=['advogado'], topn=1))

# CONTRAVENÇÃO ESTÁ PARA CRIME ASSIM COMO INFRAÇÃO ESTÁ PARA?
print(model1.wv.most_similar(positive=['contravencao', 'crime'], negative=['infracao'], topn=1))

# APELAÇÃO ESTÁ PARA SENTENÇA ASSIM COMO RECURSO ESTÁ PARA?
print(model1.wv.most_similar(positive=['apelacao', 'sentenca'], negative=['recurso'], topn=1))

print(model1.wv.similarity('juiz', 'crime'))

"""# DISCUSSÃO SOBRE OS RESULTADOS SO MODELO Skip-Gram
****
No geral, os embeddings Word2Vec treinados parecem capturar bem as relações semânticas dentro do contexto jurídico. O modelo identifica termos relacionados, compreende variações de gênero e, em muitos casos, reconhece a similaridade contextual entre termos. No entanto, há espaço para melhorias, especialmente na compreensão de analogias complexas e na distinção entre papéis jurídicos específicos. Agora falando de um contexto mais especifico, algumas analogias se saem melhor com vector_size e window menores, por exemplo:

PROMOTORA ESTÁ PARA JUIZ ASSIM COMO PROMOTOR ESTÁ PARA?

Resultado: waltraud.

O que parece ser um nome própio e não dá para saber se é um nome de advogado(a) ou juiz(a)

Quando testei com vector_size e window com valores entre 100-150 e 5-10 respectivamente, em várias casos resultou em Juiza ou similares, o que é mais adequado.

Então por quê esses parametros atuais tão elevados?! Eles demonstraram em geral gerarem resultados melhores.
"""

def sample_with_temperature(similar_words, temperature=1.0):
    words, scores = zip(*similar_words)

    probs = np.exp(np.array(scores) / temperature)
    probs /= np.sum(probs)

    return np.random.choice(words, p=probs)

def generate_text_word2vec(model, start_word, max_words=20, window_size=3, pooling_method='mean', temperature=1.0):
    generated_text = [start_word]
    used_words = set([start_word])

    for _ in range(max_words - 1):
        recent_words = generated_text[-window_size:]
        embeddings = [model.wv[word] for word in recent_words if word in model.wv]

        if not embeddings:
            break

        if pooling_method == 'mean':
            pooled_embedding = np.mean(embeddings, axis=0)
        elif pooling_method == 'sum':
            pooled_embedding = np.sum(embeddings, axis=0)
        else:
            raise ValueError("Pooling method not supported.")

        similar_words = model.wv.similar_by_vector(pooled_embedding, topn=10)
        similar_words = [(word, score) for word, score in similar_words if word not in used_words]

        if not similar_words:
            break

        next_word = sample_with_temperature(similar_words, temperature)
        generated_text.append(next_word)
        used_words.add(next_word)

    return ' '.join(generated_text)

print(generate_text_word2vec(model1, 'morte', window_size=3, pooling_method='mean', temperature=1.0))

print(generate_text_word2vec(model1, 'advogado', window_size=3, pooling_method='mean', temperature=1.0))

print(generate_text_word2vec(model1, 'pensao', window_size=3, pooling_method='mean'))

"""# AVALIAÇÃO DO TEXTO GERADO
***

**Palavra inicial "morte":** O texto gerado é coeso e parece seguir uma temática médica ou de saúde, o que faz sentido com a palavra inicial.

**Palavra inicial "advogado":** O texto gerado parece ser uma sequência nomes e sobrenomes, supondo que sejam de advogados, faz total sentido.

**Palavra inicial "pensao":** O texto parece seguir uma temática de pensão e questões relacionadas, o que faz sendido com a palavra inicial. O inicio do texto parece ser tipos de pensão ("vitalicia", "vitalicio", "pensionamento"), depois estados de pensão ("provisionar", "inabilitou", "afirmativo", "reversível", "incluiria") e por fim, coisas que podem ter causado a pensão ou fim dela ("incapacitado", "sinovite", "tendinopatia", "clinicamente").


"""

# COMPARAÇÃO DE DIFERENTES JANELAS E MÉTODOS DE POOLING
window_sizes = [2, 5, 10]
pooling_methods = ['mean', 'sum']
seed_word = 'juiz'

for window_size in window_sizes:
    for pooling_method in pooling_methods:
        print(f"Gerando texto com janela = {window_size}, pooling = {pooling_method}")
        text = generate_text_word2vec(model1, seed_word, window_size=window_size, pooling_method=pooling_method)
        print(f"Texto gerado:\n{text}\n")

"""# IMPACTO DO TAMANHO DA JANELA E DO MÉTODO DE POOLING
****

* **Tamanho da janela:**

* * **Janela = 2:** O texto gerado tende a ser mais curto e pode conter palavras que estão mais próximas do contexto imediato da palavra inicial, resultando em uma sequência mais direta e menos variada.

* * **Janela = 5:** Aumentar a janela permite considerar um contexto mais amplo resultando em uma geração de texto mais variada e possivelmente mais coerente a palavra inicial.

* * **Janela = 10:** Uma janela maior captura um contexto ainda mais amplo, o que pode resultar em uma geração de texto que inclui uma gama mais ampla de termos relacionados. O texto gerado tende a ser mais diverso.

* **Métodos de pooling:**

* * **Pooling = Mean:** Usar a média dos embeddings das palavras pode produzir um resultado que é uma combinação geral dos contextos das palavras recentes. Isso pode levar a um texto mais suave e menos repetitivo, porém pode deixar o texto mais genérico.

* * **Pooling = Sum:** Usar a soma dos embeddings pode fazer com que o texto gerado inclua termos que são mais frequêntes ou mais associados ao contextp geral das palavras recentes. Isso pode resultar em um texto mais específico, mas às vezes menos coeso.

****
# COMPARAÇÃO DE RESULTADOS
****

* **Janela = 2:**

* * **Mean Pooling:** O texto tende a ser mais coeso e incluir termos que são diretamente relacionados ao contexto imediato da palavra inicial.

* * **Sum Pooling:** O texto é geralmente mais específico e pode mostrar uma lista mais variada de termos, mas pode faltar coesão se os termos são menos relacionados.

* **Janela = 5:**

* * **Mean Pooling:** O texto gerado tende a ser mais coeso e pode incluir uma gama mais ampla de palavras, resultando em uma narrativa mais rica e variada.

* * **Sum Pooling:** O texto é mais detalhado e específico, incluindo uma gama maior de termos, o que pode ajudar a manter a relevância ao contexto.

* **Janela = 10:**

* * **Mean Pooling:** O texto é diversificado e inclui uma gama ampla de palavras, com uma boa coesão geral.

* * **Sum Pooling:** O texto é altamente variado e pode apresentar uma ampla gama de palavras, embora a coesão possa ser um pouco menor dependendo dos termos incluídos.




"""

# MODELO LSTM

!pip install tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf

vocab_size = 5000
embedding_dim = 100
max_sequence_length = 100
batch_size = 128

tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts([' '.join(doc) for doc in preprocessed_documents])
sequences = tokenizer.texts_to_sequences([' '.join(doc) for doc in preprocessed_documents])

def data_generator(sequences, batch_size, max_sequence_length, vocab_size):
    X_batch = []
    y_batch = []
    while True:
        for sequence in sequences:
            for i in range(1, len(sequence)):
                X_batch.append(sequence[:i])
                y_batch.append(sequence[i])
                if len(X_batch) == batch_size:
                    X_train = pad_sequences(X_batch, maxlen=max_sequence_length, padding='pre')
                    y_train = tf.keras.utils.to_categorical(y_batch, num_classes=vocab_size)
                    yield X_train, y_train
                    X_batch = []
                    y_batch = []
        if len(X_batch) > 0:
            X_train = pad_sequences(X_batch, maxlen=max_sequence_length, padding='pre')
            y_train = tf.keras.utils.to_categorical(y_batch, num_classes=vocab_size)
            yield X_train, y_train

model_lstm = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim),
    LSTM(128, return_sequences=True, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    Dropout(0.2),
    LSTM(128, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    Dropout(0.2),
    Dense(vocab_size, activation='softmax')
])

model_lstm.compile(loss='categorical_crossentropy', optimizer=RMSprop(learning_rate=0.0005), metrics=['accuracy'])

total_sequences = sum(len(seq) - 1 for seq in sequences)
steps_per_epoch = total_sequences // batch_size

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.keras', save_best_only=True)  # Modificado para .keras

model_lstm.fit(
    data_generator(sequences, batch_size, max_sequence_length, vocab_size),
    steps_per_epoch=steps_per_epoch,
    epochs=10,
    callbacks=[early_stopping, checkpoint]
)

model_lstm.save("modelo_lstm.keras")

def generate_text_lstm(model, tokenizer, seed_text, max_length=20, temperature=1.0):
    output_text = seed_text
    for _ in range(max_length):
        encoded_input = tokenizer.texts_to_sequences([output_text])[0]
        encoded_input = pad_sequences([encoded_input], maxlen=max_sequence_length, padding='pre')
        preds = model.predict(encoded_input, verbose=0)[0]

        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds + 1e-10) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)

        predicted_word_index = np.random.choice(range(len(preds)), p=preds)
        predicted_word = tokenizer.index_word.get(predicted_word_index, '')

        if predicted_word == '':
            break
        output_text += ' ' + predicted_word
    return output_text

print(generate_text_lstm(model_lstm, tokenizer, 'juiz', max_length=20, temperature=0.5))

print(generate_text_lstm(model_lstm, tokenizer, 'morte', max_length=20, temperature=0.5))

print(generate_text_lstm(model_lstm, tokenizer, 'juiz', max_length=20, temperature=1.0))

print(generate_text_lstm(model_lstm, tokenizer, 'morte', max_length=20, temperature=1.0))

print(generate_text_lstm(model_lstm, tokenizer, 'juiz', max_length=20, temperature=1.5))

print(generate_text_lstm(model_lstm, tokenizer, 'morte', max_length=20, temperature=1.5))

"""# AVALIAÇÃO DOS RESULTADOS COM DIFERENTES VALORES DE TEMPERATURA
****
* **Temperatura = 0.5:**

* * **Palavra inicial = juiz:** Com uma temperatura de 0.5, o modelo tende a gerar um texto com termos comuns e estruturas que são mais previsíveis. O resultado é um texto que faz sentido em um contexto jurídico, mencionando processos como "apelação", "sentença" e "vara cível". A coerência é alta, mas o texto é relativamente repetitivo e previsível, indicando um menor nível de criatividade.

* * **Palavra inicial = morte:** O texto gerado também é coerente, mas bastante restrito a frases e palavras comuns no contexto jurídico, como "apelação cível", "vara", e "comarca". Este resultado mostra que o modelo com temperatura 0.5 produz um texto com boa gramática, mas pouca variação criativa.


* **Temperatura = 1.0:**


* * **Palavra inicial = juiz:** Aumentar a temperatura para 1.0 aumenta a diversidade de palavras e expressões utilizadas. O texto ainda é coerente e contém frases típicas do contexto jurídico, como "negarem provimento ao recurso", "sentença", e "legalidade". A maior temperatura aqui permite uma geração de texto mais variada, mantendo a coerência.

* * **Palavra inicial = morte:** O texto gerado é mais variado, mencionando termos específicos como "seguro passivo", "CPF", e "apelantes suspender". A coerência permanece boa, e a gramática é consistente. A temperatura 1.0 atinge um equilíbrio entre diversidade e coerência.

* **Temperatura = 1.5:**

* * **Palavra inicial = juiz:** Com uma temperatura de 1.5, o texto se torna significativamente mais criativo, mas a coerência começa a diminuir. Frases como "estado mateus milton figuram" e "despeito ilicitude ostenta poder brasileira" não são semanticamente claras ou esperadas no contexto jurídico. Este valor de temperatura proporciona maior diversidade, mas reduz a consistência e a lógica do texto.

* * **Palavra inicial = morte:** O texto gerado é ainda mais diversificado, incluindo termos inesperados como "nbsp" (possivelmente um artefato de processamento) e "colendo", que são menos comuns e podem não fazer sentido em conjunto. Este nível de temperatura resulta em um texto que é menos previsível, mas também menos coeso e gramaticalmente correto.


"""