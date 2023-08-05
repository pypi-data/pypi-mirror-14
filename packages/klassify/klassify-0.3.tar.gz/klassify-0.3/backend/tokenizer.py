from nltk import wordpunct_tokenize, PorterStemmer
from nltk.corpus import stopwords

stop = stopwords.words('english')
porter = PorterStemmer()


def tokenize(text):
    words = wordpunct_tokenize(text)
    stemmed = [porter.stem(word) for word in words]
    return [
        word.lower()
        for word in stemmed
        if word not in stop
        and word.isalpha()
        and len(word) > 2
    ]
