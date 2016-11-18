from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk





class PreprocessManager:

    def __init__(self):
        pass

    # Static method to get the word counts
    @staticmethod
    def get_word_counts(input_str, limit = 100):
        wordnet_lemmatizer = WordNetLemmatizer()
        snowball_stemmer = EnglishStemmer()
        tokenized_text = CountVectorizer().build_tokenizer()(input_str.lower())
        tokenized_text = [word for word in tokenized_text if len(word) > 1]  # Filter some small words
        #tokenized_text = [word for word in tokenized_text if not word.isnumeric()]
        filtered_words = [word for word in tokenized_text if word not in stopwords.words('english')]
        stemmed_list = [wordnet_lemmatizer.lemmatize(w) for w in filtered_words]
        # Calculate frequency distribution
        frequency_dist = nltk.FreqDist(stemmed_list)

        # Output top 50 words
        result = dict()
        for word, frequency in frequency_dist.most_common(limit):
            # print(u'{};{}'.format(word, frequency))
            result[word] = frequency
        return result



    # This function just splits the words and gives the words that's all!
    @staticmethod
    def get_raw_tokenized_text(input_str):
        tokenized_text = CountVectorizer().build_tokenizer()(input_str.lower())
        return tokenized_text




    # Get the stemmed list
    @staticmethod
    def get_unique_words(input_str):
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenized_text = CountVectorizer().build_tokenizer()(input_str.lower())
        tokenized_text = [word for word in tokenized_text if len(word) > 1]  # Filter some small words
        # tokenized_text = [word for word in tokenized_text if not word.isnumeric()]
        filtered_words = [word for word in tokenized_text if word not in stopwords.words('english')]
        snowball_stemmer = EnglishStemmer()
        stemmed_list = [wordnet_lemmatizer.lemmatize(w) for w in filtered_words]
        return set(stemmed_list)




