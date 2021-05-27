import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    os.chdir(directory)
    corpus = {}
    for i in [f for f in os.listdir() if f.endswith(".txt")]:
        files = os.path.join(os.getcwd(), i)
        text = open(files, "r", encoding="utf8")
        content = text.read()
        corpus[i] = content
    
    return corpus

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    punctuations = string.punctuation
    tokens = nltk.word_tokenize(document.lower())
    for i in list(tokens):          #iterating in a copy, since removing the original while iterating through it can skip the element. The iterator continutes, while indexes changes.
        if i in stopwords:
            tokens.remove(i)
        if i in punctuations:
            tokens.remove(i)
        
    return tokens

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    '''
    idf = {}
    number = len(documents)
    for i in documents.keys():
        # for each word in each document, add the word into the idf count in the dictionary if it exists, else create it and set the count to 1.
        for word in set(documents[i]):
            if word in idf.keys():
                idf[word] += 1
            else:
                idf[word] = 1
    
    #calculate the idf from the occurence of the document with the word and the number of documents (len(documents))
    for word in idf.keys():
        idf[word] = math.log(number / idf[word])
    
    return idf
    '''
    #get idfs for eahc value
    idfs = {}
    for i in documents.keys():
        for word in set(documents[i]):
            # get the sum of occurence of the files where the word occur
            f = sum(word in documents[filename] for filename in documents)
            # calculate the idf
            idf = math.log(len(documents) / f)
            idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    #get TF-IDFs
    tfidfs = {}
    #set the TF-IDF for each file at 0
    for filename in files.keys():
        tfidfs[filename] = 0
        #for each word in the query, add the TF-IDF of the word to the file
        for word in query:
            tf = files[filename].count(word)
            tfidfs[filename] += (tf * idfs[word])           #TF-IDF is the product of TF and IDF

    return sorted(tfidfs, key=tfidfs.get, reverse=True)[:n] #return the top n tfidfs in revese order according to the value (tfidfs.get)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sum_idf = {}
    #idf_word = {}              #check idf of word in query
    for i in sentences.keys():
        #for each sentence, create a dictionary entry with a list of two scores. The first one represents idf and the second one represents density
        sum_idf[i] = [0, 0]
        query_in_sentence = 0
        for word in query:
            if word in sentences[i]:
                query_in_sentence += 1
                sum_idf[i][0] += idfs[word]
                #idf_word[word] = idfs[word]            #check idf of word in query
        sum_idf[i][1] = (query_in_sentence / len(sentences[i]))
 
    return sorted(sum_idf, key=lambda k: (sum_idf[k][0], sum_idf[k][1]), reverse=True)[:n]      #set lambda, to two variables to sort by.

    '''
    #check the idf and density of the sentences
    return sorted(sum_idf.items(), key=lambda t: t[1][0], reverse=True)[:5]

    #check the idf of the words in the query
    return idf_word.items()

    #check the sentence tokenization
    test = []
    for i in sorted(sum_idf, key=sum_idf.get, reverse=True)[:5]:
        test.append(sentences[i])
    
    return test
    '''


if __name__ == "__main__":
    main()
