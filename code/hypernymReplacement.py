import re

import spacy
from nltk.corpus import wordnet as wn
# from tqdm.auto import tqdm



# create filtered synsets
def get_synsets(word:spacy.tokens.token.Token, pos_tag_dict: dict):
    try:
        pos_tag= pos_tag_dict[word.pos_]
        wordnet_synsets = wn.synsets(word.text, pos=pos_tag)
    except KeyError:
        wordnet_synsets = []
    return wordnet_synsets

# filter out best synset
def find_best_synset(document: spacy.tokens.doc.Doc, sentence:spacy.tokens.span.Span, list_of_synsets):
    synset_names = [synset.name().split(".")[0] for synset in list_of_synsets]
    synset_names = [name.replace("_", " ") for name in synset_names]
    synset_vocab = [document.vocab[name] for name in synset_names]
    similarities = [sentence.similarity(name) for name in synset_vocab]
    max_sim = max(similarities)
    synset_index = similarities.index(max_sim)
    best_synset = list_of_synsets[synset_index]
    # print("find_best_synset: ", best_synset, max_sim)
    return best_synset

def alternate_best_hypernym(synset):
    hypernyms = synset.hypernyms()
    similarities = [synset.wup_similarity(hypernym) for hypernym in hypernyms]
    max_sim = max(similarities)
    synset_index = similarities.index(max_sim)
    best_hypernym = hypernyms[synset_index]
    # print("alternate_best_hypernym: ", best_hypernym, max_sim)
    return best_hypernym



def replace_with_hypernym(vocab_list: list, document: spacy.tokens.doc.Doc) -> str:
    """Replaces 'complex' words (defined as words from the B2/C1/C2 readers level from CEFR-J) with their first hypernyms from wordnet

    Input: document from spacy (spacy.tokens.doc.Doc)

    Output: document with complex words replaced with hypernyms, type string
    """
    pos_tag_dict = {'NOUN':'n',
                    'VERB':'v',
                    'ADJ' :'a',
                    'ADJ' :'s',
                    'ADV' :'r'}
    new_document = document.text
    sentences = document.sents
    for sentence in sentences:
        for word in sentence:
            word_text = word.text
            if word_text in vocab_list:
                # implementation of empty snysets
                # print(word_text)  
                synset_list = get_synsets(word, pos_tag_dict)
                if synset_list:
                    right_synset = find_best_synset(document, sentence, synset_list)
                    hypernym_list = right_synset.hypernyms()
                    if hypernym_list:
                        right_hypernym = alternate_best_hypernym(right_synset)
                        right_hypernym2 = find_best_synset(document, sentence, hypernym_list)
                        name = right_hypernym.name()
                        new_word = name.split(".")[0]
                        if "_" in new_word:
                            new_word = new_word.replace("_", " ")
                        # print(word_text, " => ", new_word, "\nSentence: ", sentence)
                        new_document = re.sub(
                            word.text + r"\b", new_word, new_document
                            )  # to catch accidental in-word-replacements
    return new_document

