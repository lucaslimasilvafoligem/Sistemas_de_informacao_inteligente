# -*- coding: utf-8 -*-
"""Cópia de Processamento de Texto (Alunos).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YKuu34piukSEku59jV5Ub-eWiaVZQfSJ

# Processamento de Texto

Nesse notebook, nós vamos ver na prática como podemos aplicar algumas técnicas de processamento de texto programaticamente, usando algumas bibliotecas conhecidas.

## NLTK

Vamos começar usando a biblioteca  [NLTK (Natural Language Toolkit)](https://www.nltk.org/).

Primeiramente, vamos importar as bibliotecas python que vamos usar nesse tutorial:
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

# %matplotlib inline

"""e vamos fazer o download de alguns módulos específicos do NLTK:"""

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

"""### Tokenization

#### Sentence Tokenization
"""

text = """Hello Mr. Smith, how are you doing today?
    The weather is great, and city is awesome.
    The sky is pinkish-blue. You shouldn't eat cardboard
"""

tokenized_sent = sent_tokenize(text)
print(tokenized_sent)

"""Nós também podemos tokenizar outras linguas:"""

portuguese_text = "Bom dia, Sr. Smith. Como você está? O tempo está bom, e a cidade maravilhosa."

print(sent_tokenize(portuguese_text, "portuguese"))

"""#### Word Tokenization"""

tokenized_word = word_tokenize(text)
print(tokenized_word)

"""No exemplo acima, a tokenização de palavras foi aplicada ao texto inteiro. Porém, normalmente, o fluxo adotado é aplicar a tokenização nas sentenças e, em seguida, aplicar nas palavras de cada sentença.

### Remoção de Pontuação

Remova a pontuação das sentenças 'tokenizadas', antes de aplicar o tekenizador de palavras.

**Veja exemplos abaixo:**

**EXEMPLO 1**

Um dos [tipos de tokenizer oferecidos pelo NLTK](http://www.nltk.org/api/nltk.tokenize.html) é baseado em Expressões Regulares (Regex).
Então, por exemplo, você pode definir um tokenizer que detecta sequências de caracteres alfanuméricos como tokens e descarta todo o resto:
"""

from nltk.tokenize import RegexpTokenizer

text = """Hello Mr. Smith, how are you doing today?
    Here the weather is great, the temperature is 25 degrees celsius and today's IR Lab is awesome.
    You should come and enjoy this joy-filled environment!
"""

tokenized_sent = sent_tokenize(text)

tokenizer = RegexpTokenizer(r'\w+') #ou r'[a-zA-Z]+' se não quiser incluir números e underscore, pois \w+ equivale a [a-zA-Z0-9_]+
for sent in tokenized_sent:
  sent_without_punct = tokenizer.tokenize(sent)
  print(sent_without_punct)

"""**EXEMPLO 2**

Ou dessa outra forma, em puro python:
"""

import string
text = """Hello Mr. Smith, how are you doing today?
    Here the weather is great, the temperature is 25 degrees celsius and today's IR Lab is awesome.
    You should come and enjoy this joy-filled environment!
"""
unicode_translate_table = dict((ord(char), None) for char in string.punctuation)

tokenized_sent = sent_tokenize(text)

for sent in tokenized_sent:
  sent_without_punct = sent.translate(unicode_translate_table)
  print(sent_without_punct)

"""**EXEMPLO 3**

Uma outra alternativa é usar `isalpha()` ou `isalnum()`. Neste caso, você deve aplicar depois da tokenização de palavras, para remover as que não se adequem.
"""

text = """Hello Mr. Smith, how are you doing today?
    Here the weather is great, the temperature is 25 degrees celsius and today's IR Lab is awesome.
    You should come and enjoy this joy-filled environment!
"""

tokens = [word.lower() for sent in sent_tokenize(text) for word in word_tokenize(sent) if word.isalnum()] #também converte para lowercase
print(*tokens)

"""### Expanção das contrações (contractions)

"""

import contractions

contractions.fix("I'll show you a simple example, it's easy to understand. \
I don't wanna show anything else because I'm lazy. I'm gonna stop writing now. \
I'd love to stay, but I've got to go! I gotta go! Shouldn't you go too? \
No, I know you are enjoying today's IR Lab!!")

"""### Frequency Distribution"""

fdist = FreqDist(tokenized_word)
print(fdist)

fdist

fdist.most_common(5)

fdist.plot(30, cumulative=False)
plt.show()

"""### Stopwords"""

stop_words = set(stopwords.words("english"))

print(stop_words)

"""**TODO**: A partir da lista de palavras tokenizadas acima, gere uma nova lista de palavras que não contém stop words (use list  comprehension)"""

filtered_words = [word for word in tokenized_word if word.lower() not in stop_words]

print("Tokenized Words:", tokenized_word)
print("Filterd Sentence:", filtered_words)

"""### Stemming

A **Stemming** reduz as palavras aos seus radicais. Por exemplo, as palavras *connection*, *connected*, *connecting* serão reduzidas a "*connect*". Há diversos algoritmos de stemming, mas o mais famoso é o `Porter stemming`.
"""

example_words = ['connection', 'connected', 'connecting']

ps = PorterStemmer()

stemmed_words = [ps.stem(w) for w in example_words]

print("Example words:", example_words)
print("Stemmed words:", stemmed_words)

"""O algoritmo `SnowBall` pode faz o processo de stemming em até 13 línguas diferentes:"""

print(SnowballStemmer.languages)

"""Vamos ver como funciona em português!

**TODO:** Crie 4 listas de palavras em português contendo radicais similares (cada lista deve conter ao menos 2 palavras - preferencialmente 3 ou mais).

Para cada uma das listas, gere uma outra lista com termos equivalentes "stemizados".

Suas listas originais devem conter palavras que gerem stems do tipo: verdadeiros positivos, verdadeiros negativos, falsos positivos, falsos negativos.

tp = você acha que o resultado do stemmer deve ser os mesmo para todos os termos da lista (e confirma que é em tp_stemmed)

tn = mas você acha que o resultado do stemmer deve ser diferente para todos os termos da lista, embora os radicais sejam similares (e confirma que são em tn_stemmed)

fp = você acha que o resultado do stemmer deve ser diferente para todos os termos da lista (mas percebe em fp_stemmed que são iguais)

fn = você acha que o resultado do stemmer deve ser igual para todos os termos da lista (mas percebe em fn_stemmed que são diferentes)
"""

tp = ['correr', 'corrida', 'correu']
tn = ['cantar', 'cantora', 'cantarola']
fp = ['beber', 'bebida', 'bebi']
fn = ['andar', 'andou', 'andava']

ss = SnowballStemmer("portuguese")

tp_stemmed = [ss.stem(word) for word in tp]
tn_stemmed = [ss.stem(word) for word in tn]
fp_stemmed = [ss.stem(word) for word in fp]
fn_stemmed = [ss.stem(word) for word in fn]

print('TP Stemmed:', tp_stemmed)
print('TN Stemmed:', tn_stemmed)
print('FP Stemmed:', fp_stemmed)
print('FN Stemmed:', fn_stemmed)

"""### Lemmatization

Vamos comparatar a saída do Stemmer e do Lemmatizer
"""

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer( )
for item in ['am' ,'are' ,'is','was','were']:
    print(stemmer.stem(item),end='\t')

lemmatizer = WordNetLemmatizer( )
for item in ['am' ,'are' ,'is','was','were']:
    print(lemmatizer.lemmatize(item),end='\t')

"""Esperava uma resposta diferente acima? Esperava que as saídas fossem todas "be" ?

Esse problema acontece porque o lamatizador não sabe que estamos tratando de um verbo!

**TODO:** Faça um código equivalente ao anterior (trecho da lematização), porém, passando o valor 'v' (Verbo) no parâmetro `pos` (Part-Of-Spreech).
"""

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

for item in ['am', 'are', 'is', 'was', 'were']:
    print(lemmatizer.lemmatize(item, pos='v'), end='\t')

"""**TODO:** Agora faça um código equivalente ao anterior, porém, passando a constante wordnet.VERB no parâmetro `pos` (Part-Of-Spreech).  """

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()

for item in ['am', 'are', 'is', 'was', 'were']:
    print(lemmatizer.lemmatize(item, pos=wordnet.VERB), end='\t')

"""### POS Tagging

Conjunto de Tags Baseado no [Penn Treebank Tag Set](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
"""

sent = "Albert Einstein was born in Ulm, Germany, in 1879."

tokens = nltk.word_tokenize(sent)
print('Sentence:', tokens)
print(nltk.pos_tag(tokens))

"""**TODO:** Formule uma frase (mesmo que não faça sentido) de forma que o POS Tagger classifique 'Albert' como verbo."""

import nltk

# Sentença com 'Albert' como verbo
sentenca = "He Albert the problem away."
tokens = nltk.word_tokenize(sentenca)
tagged = nltk.pos_tag(tokens)
print("Sentence:", tokens)
print(tagged)

"""**TODO:** Agora formule duas sentenças (que façam sentido) onde a mesma palavra é classificada de uma forma na sentença 1 e de outra forma na sentença 2."""

import nltk

# Sentença 1
sentenca1 = "The wind blows gently through the leaves of the trees."
tokens1 = nltk.word_tokenize(sentenca1)
tagged1 = nltk.pos_tag(tokens1)
print(tagged1)

# Sentença 2
sentenca2 = "Please, wind, don't wind so strongly."
tokens2 = nltk.word_tokenize(sentenca2)
tagged2 = nltk.pos_tag(tokens2)
print(tagged2)

"""### Lemmatization com POS-Tagging

Vamos automatizar o processo de lematização: vamos detectar a POS-TAG com nltk.pos_tag e então passá-la para o wordnet lemmatizer.

Execute o comando abaixo para criar as classes necessárias. Analise o código para entender.
"""

# observe e o que o código abaixo faz

class Splitter(object):
    """
    split the document into sentences and tokenize each sentence
    """
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self,text):
        """
        out : ['What', 'can', 'I', 'say', 'about', 'this', 'place', '.']
        """
        # split into single sentence
        sentences = self.splitter.tokenize(text)
        # tokenization in each sentences
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]
        return tokens


class LemmatizationWithPOSTagger(object):
    def __init__(self):
        pass
    def get_wordnet_pos(self,treebank_tag):
        """
        return WORDNET POS compliance to WORDNET lemmatization (a,n,r,v)
        """
        if treebank_tag.startswith('A'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def pos_tag_lemma_complete(self,tokens):
        lemmatizer = WordNetLemmatizer()
        # find the pos tag for each token [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = [nltk.pos_tag(token) for token in tokens]

        # lemmatization using pos tag
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        pos_tokens = [ [(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens

    def pos_tag_lemma_basic(self,tokens):
        lemmatizer = WordNetLemmatizer()
        # find the pos tag for each token [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = [nltk.pos_tag(token) for token in tokens]

        # lemmatization using pos tag
        # convert into list of Lemmatized words
        pos_tokens = [ [lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens

"""Agora complete o código abaixo com o que se pede:"""

# Instanciando um objeto de cada classe
splitter = Splitter()
lemmatizer = LemmatizationWithPOSTagger()

# Texto de exemplo
text = "This is a sample text. It contains multiple sentences."

# Passo 1: Usando o splitter e imprimindo o resultado
print("Resultado do Splitter:")
tokens = splitter.split(text)
for sentence_tokens in tokens:
    print(sentence_tokens)

# Criando uma instância da classe LemmatizationWithPOSTagger
lemmatizer = LemmatizationWithPOSTagger()

# Passo 2: Usando o lematizador básico e imprimindo o resultado
print("\nResultado do Lematizador Básico:")
lemma_basic_tokens = lemmatizer.pos_tag_lemma_basic(tokens)
for sentence_lemma_tokens in lemma_basic_tokens:
    print(sentence_lemma_tokens)

# Passo 3: Usando o lematizador completo e imprimindo o resultado
print("\nResultado do Lematizador Completo:")
lemma_complete_tokens = lemmatizer.pos_tag_lemma_complete(tokens)
for sentence_lemma_tokens in lemma_complete_tokens:
    print(sentence_lemma_tokens)

"""## Outras Bibliotecas

Vamos conhecer outras libs que nos ajudam nesse tipo de tarefa

### Lematização usando [Stanza](https://stanfordnlp.github.io/stanza/)
"""

"""**TODO:** complete o código abaixo"""

import stanza
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma')

# Seu código aqui
# Substitua a string vazia por uma sequencia de termos separados por espaço)
doc = nlp('The quick brown fox jumps over the lazy dog')

# Seu código aqui
# Imprima lado a lado os termos com seus repectivos lemas
# Em uma única expressão usando list comprehension, gere o lemas para os termos acima, manipulando doc.sentences, doc.sentences.words
# O texto e o lema podem ser obtidos com .text e .lemma em cada item (cada word em doc.sentences.words)
# Carregar o pipeline para o idioma inglês

# Imprimir lado a lado os termos com seus respectivos lemas
print([(word.text, word.lemma) for sent in doc.sentences for word in sent.words])

"""### Lematização usando [Spacy](https://spacy.io) - [lemminflect](https://spacy.io/universe/project/lemminflect/)"""


"""**TODO:** Complete o código"""

import spacy
import lemminflect

nlp = spacy.load('en_core_web_sm')
doc = nlp('best well better be was were is am')

# aqui podemos iterar em 'doc'
print(f"{'Text':{8}} | {'Lemma':{6}}\n")
for token in doc:
    print(f"{token.text:{8}} | {lemminflect.getLemma(token.text, 'VERB')[0]:{6}}")

"""#### Função getLemma"""

from lemminflect import getLemma
getLemma( 'watches', upos='VERB')

"""## N-Gramas

### Implementação ad-hoc (função que gera os n-gramas a partir da lista de tokens)
"""

def n_grams(tokens,ngram=1):
  temp=zip(*[tokens[i:] for i in range(0,ngram)])
  result=[' '.join(ngram) for ngram in temp]
  return result

"""**TODO:** Produza um exemplo para um texto qualquer. Primeiro, defina uma forma de tokenizar o texto e depois gere os n-gramas que desejar com a função acima."""

def n_grams(tokens, ngram=1):
    temp = zip(*[tokens[i:] for i in range(0, ngram)])
    result = [' '.join(ngram) for ngram in temp]
    return result

# Texto de exemplo
text = '''Imagination is more important than knowledge.'''

# Tokenizar o texto
tokens = text.split()

# Gerar n-gramas para n=1 (unigrama), n=2 (bigrama) e n=3 (trigrama)
unigrams = n_grams(tokens, ngram=1)
bigrams = n_grams(tokens, ngram=2)
trigrams = n_grams(tokens, ngram=3)
hexagrams = n_grams(tokens, ngram=6)

# Imprimir os resultados
print("Unigrams:", unigrams)
print("Bigrams:", bigrams)
print("Trigrams:", trigrams)
print("Hexagramas:", hexagrams)

"""### Usando NLTK

Observe o código a seguir:
"""

from nltk.util import ngrams

text = '''Hello Mr. Smith, how are you doing today?
    The weather is great, and city is awesome.
    The sky is pinkish-blue. You shouldn't eat cardboard
'''

tokens = [word.lower() for sent in sent_tokenize(text) for word in word_tokenize(sent) if word.isalnum()]

list(ngrams(tokens, 3))

"""A saída do código acima não é igual à nossa implementação ad-hoc. O código abaixo torna a saída igual à nossa (o nltk não retorna a string, mas sim o zip). Adicione uma linha de código no final, apenas para imprimir o resultado."""

temp=ngrams(tokens, 3)
result=[' '.join(ngram) for ngram in temp]
print(result)