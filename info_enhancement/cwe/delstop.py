from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string
import jieba

def wash_sentence(unwashed):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(unwashed.lower()) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words and not w in string.punctuation] 
    return ' '.join(filtered_sentence)

def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    stop_words = set(stopwords.words('english')) 
    return ' '.join(list(filter(lambda x: x not in stop_words and x not in string.punctuation and x != ' ', seg_result)))

if __name__ == '__main__':
    example_sent = "This is a sample sentence, showing off the stop words filtration." 
    print(wash_sentence(example_sent))