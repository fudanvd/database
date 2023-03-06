from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_util(corpus):
    tfidf_vec = TfidfVectorizer()

    tfidf_matrix = tfidf_vec.fit_transform(corpus)
    return tfidf_matrix
    #print(tfidf_vec.get_feature_names_out())
    #print(tfidf_vec.vocabulary_)

if __name__ == '__main__':
    testcorpus = [
        "What is the weather like today",
        "what is for dinner tonight",
        "this is question worth pondering",
        "it is a beautiful day today"
    ]   
    tfidf_util(testcorpus)