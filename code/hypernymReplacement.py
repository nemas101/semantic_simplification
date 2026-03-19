import re

import spacy
from nltk.corpus import wordnet as wn
from tqdm.auto import tqdm

# dictionary of pos tags, keys = Wordnet pos tags, values = spacy pos tags (Universal dependencies)
pos_tag_dict = {'NOUN':'n',
                'VERB':'v',
                'ADJ' :'a',
                'ADJ' :'s',
                'ADV' :'r'}

# create filtered synsets
def get_synsets(word:spacy.tokens.token.Token, pos_tag_dict: dict):
    print(word.text)
    pos_tag= pos_tag_dict[word.pos_]
    wordnet_synsets = wn.synsets(word.text, pos=pos_tag)
    return wordnet_synsets

# filter out best synset
def find_best_synset(document: spacy.tokens.doc.Doc, sentence:spacy.tokens.span.Span, list_of_synsets):
    synset_names = [synset.name().split(".")[0] for synset in list_of_synsets]
    synset_vocab = [document.vocab[name] for name in synset_names]
    similarities = [sentence.similarity(name) for name in synset_vocab]
    max_sim = max(similarities)
    synset_index = similarities.index(max_sim)
    best_synset = list_of_synsets[synset_index]
    return best_synset



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
        for word in tqdm(sentence):
            word_text = word.text
            if word_text in vocab_list:
                # implementation of empty snysets
                synset_list = get_synsets(word, pos_tag_dict)
                if len(synset_list) > 0:
                    right_synset = find_best_synset(document, sentence, synset_list)
                    hypernym_list = right_synset.hypernyms()
                    if len(hypernym_list) > 0:
                        right_hypernym = find_best_synset(document, sentence, hypernym_list)
                        name = right_hypernym.name()
                        new_word = name.split(".")[0]
                        if "_" in new_word:
                            new_word = new_word.replace("_", " ")
                        new_document = re.sub(
                            word_text + "\b", new_word, new_document
                    )  # to catch accidental in-word-replacements
    breakpoint()
    return new_document

