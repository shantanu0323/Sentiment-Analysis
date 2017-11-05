import nltk

nltk.download('punkt')
def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})

print(format_sentence("The cat is very cute"))

pos = []
with open("./pos_tweets.txt") as f:
    for i in f:
        pos.append([format_sentence(i), 'pos'])

neg = []
with open("./neg_tweets.txt") as f:
    for i in f:
        neg.append([format_sentence(i), 'neg'])

# next, split labeled data into the training and test data
training = pos[:int((.8) * len(pos))] + neg[:int((.8) * len(neg))]
test = pos[int((.8) * len(pos)):] + neg[int((.8) * len(neg)):]

from nltk.classify import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(training)

classifier.show_most_informative_features()

example1 = "Cats are awesome!"

print(classifier.classify(format_sentence(example1)))

from nltk.classify.util import accuracy
print(accuracy(classifier, test))

