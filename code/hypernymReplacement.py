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
def find_synsets(word:spacy.tokens.token.Token, pos_tag_dict: dict):
    pos_tag= pos_tag_dict[word.pos_]
    wordnet_synsets = wn.synsets(word.text, pos=pos_tag)
    return wordnet_synsets

# create hypernyms
def find_best_synset(sentence:spacy.tokens.span.Span, word:spacy.tokens.token.Token, pos_tag_dict: dict):
    wordnet_synsets = find_synsets(word, pos_tag_dict)
    return wordnet_synsets

# filter out best solution




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
                right_synsets = find_best_synset(sentence, word, pos_tag_dict)
                # maybe filtering by pos-tags for better hypernyms
                breakpoint()
                hypernym_list = right_synsets[0].hypernyms()
                if len(hypernym_list) > 0:
                    hypernym = hypernym_list[0]
                    word_hypernym_synset = hypernym
                    name = word_hypernym_synset.name()
                    new_word = name.split(".")[0]
                    if "_" in new_word:
                        new_word = new_word.replace("_", " ")
                    new_document = re.sub(
                        word_text + "\b", new_word, new_document
                    )  # to catch accidental in-word-replacements
    breakpoint()
    return new_document

