from rake_nltk import Rake                    #rake-nltk is a library didi
import nltk                                   #nltk - Natural Language Toolkit didi
nltk.download('stopwords')

nltk.download('punkt')                  #punkt - tokenizer model helps to split teh sentences did
text = """
Artificial Intelligence and machine learning are transforming the tech industry.
Many applications, from chatbots to recommendation systems, use AI in some form.
"""
rake = Rake(language='english')                         #creating instance
rake.extract_keywords_from_text(text)
keywords_with_scores = rake.get_ranked_phrases_with_scores()
print("Top Keywords:")
for score,phrase in keywords_with_scores:
    print(f"{score:.2f} - {phrase}")
