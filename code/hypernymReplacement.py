import re

import spacy
from nltk.corpus import wordnet as wn
from tqdm.auto import tqdm


def replace_with_hypernym(vocab_list: list, document: spacy.tokens.doc.Doc) -> str:
    """Replaces 'complex' words (defined as words from the B2/C1/C2 readers level from CEFR-J) with their first hypernyms from wordnet

    Input: document from spacy (spacy.tokens.doc.Doc)

    Output: document with complex words replaced with hypernyms, type string
    """
    new_document = document.text
    for word in tqdm(document):
        word_text = word.text
        if word_text in vocab_list:
            synset = wn.synsets(word_text)
            if len(synset) > 0:
                # pos = synset[0].pos()
                # maybe filtering by pos-tags for better hypernyms
                hypernym_list = synset[0].hypernyms()
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
    return new_document