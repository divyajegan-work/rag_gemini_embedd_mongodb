import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from gensim.models import Word2Vec
documents = [
    "The cat sat on the mat.",
    "The dog sat on the log.",
    "Cats and dogs are great pets.",
    "I love my cat and my dog."
]
# 1. One-Hot Encoding
# Create a vocabulary
vocabulary = list(set(word.lower() for doc in documents for word in doc.split()))
ohe = OneHotEncoder(sparse_output=False)
one_hot_encoded = ohe.fit_transform(np.array(vocabulary).reshape(-1, 1))    #If there are 10 words, the output will be a 10×10 matrix where each row is a one-hot vector.
print("One-Hot Encoding:")
print(pd.DataFrame(one_hot_encoded, columns=ohe.get_feature_names_out(), index=vocabulary))
# 2. Bag of Words (BoW) (each sentence - documents and words in that sentence is 1 else 0)(uses for )
bow_vectorizer = CountVectorizer()
bow_matrix = bow_vectorizer.fit_transform(documents).toarray()
print("\nBag of Words (BoW):")
print(pd.DataFrame(bow_matrix, columns=bow_vectorizer.get_feature_names_out()))
# 3. Term Frequency-Inverse Document Frequency (TF-IDF)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents).toarray()
print("\nTF-IDF:")
print(pd.DataFrame(tfidf_matrix, columns=tfidf_vectorizer.get_feature_names_out()))
# 4. Word2Vec
# Preprocess the documents into a list of lists for Word2Vec  window is to learn nearby words to undrstand
tokenized_docs = [doc.lower().split() for doc in documents]
word2vec_model = Word2Vec(tokenized_docs, vector_size=100, window=5, min_count=1, workers=4)
# Displaying the wordpyth vectors
print("\nWord2Vec Vectors:")
for word in word2vec_model.wv.index_to_key:
    print(f"{word}: {word2vec_model.wv[word]}")
