import argparse
import re

import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from tqdm.auto import tqdm

# if necessary run there once:
# nltk.download("punkt_tab")
# nltk.download("wordnet")


def spacyfy_text(text) -> list[str]:
    n = 99999  # set for spacys maximal text limit
    chunks = [text[i : i + n] for i in range(0, len(text), n)]
    sentences = []
    for chunk in tqdm(chunks):
        chunk_spacyfied = [sentence for sentence in nlp(chunk).sents]
        sentences.extend([sentence.text for sentence in chunk_spacyfied])

    return sentences


def replace_with_hypernym(vocab_list, document):
    """Replaces 'complex' words (defined as words from the B2/C1/C2 readers level from CEFR-J) with their first hypernyms from wordnet"""
    # word_list = [w.text for w in document]
    # maybe lemmatize for all the verbs?
    # lemma_list = [lemmatizer.lemmatize(word) for word in word_list]
    new_document = document.text
    for word in tqdm(document):
        word_text = word.text
        # lemma = lemmatizer.lemmatize(word_text)
        # if lemma in vocab_list:
        if word_text in vocab_list:
            synset = wn.synsets(word_text)
            if len(synset) > 0:
                hypernym_list = synset[0].hypernyms()
                if len(hypernym_list) > 0:
                    hypernym = hypernym_list[0]
                    word_hypernym_synset = hypernym
                    name = word_hypernym_synset.name()
                    new_word = name.split(".")[0]
                    if "_" in new_word:
                        new_word = new_word.replace("_", " ")
                    new_document = new_document.replace(word_text, new_word)
    return new_document


def find_adjectives_before_nouns(document):
    """
    Finds any adjectives in attributive position before a noun

    Input: spacy-document of the text (spacy.tokens.doc.Doc')

    Output: dict of of the adjectives to be replaces (items: adjective and noun, values: only nouns)
    """
    pattern_adj_noun = [[{"POS": "ADJ"}, {"POS": "NOUN"}]]
    pattern_noun = [[{"POS": "ADJ"}]]

    matcher.add("adj_noun", pattern_adj_noun)  # matches all adj-noun combinations
    matcher.add("only_adj", pattern_noun)  # matches all adjectives

    matches = matcher(document)
    filtered_adj_matches = {}
    prev_match = (0, 0, 0)

    for match_id, start, end in matches:
        if start == prev_match[1]:
            filtered_adj_matches[document[start:end].text] = document[start + 1 : end].text
            # string_id = nlp.vocab.strings[match_id]
            # span = document[start:end]
            # print(match_id, string_id, start, end, span.text) #test for the match
            # print("Filtered Word :", document[start:end-1]) # test for the adjective to be filtered
            # print(filtered_adj_matches[-1])
        prev_match = (match_id, start, end)

    matcher.remove("adj_noun")  # matches all adj-noun combinations
    matcher.remove("only_adj")

    # breakpoint()
    return filtered_adj_matches


def find_adverbs(document):
    """
    Finds any adverbs in a given document

    Input: spacy-document of the text (spacy.tokens.doc.Doc')

    Output: list of of the adverbs to be replaces (list of str)
    """
    pattern_adv = [[{"POS": "ADV"}]]

    matcher.add("adv", pattern_adv)  # matches all adverbs

    matches = matcher(document)
    filtered_adv_matches = {}

    for _, start, end in matches:
            filtered_adv_matches[document[start:end].text] = ""

    return filtered_adv_matches

def replace_words(document,removal_dict):
    """Replaces words in a document according to a given removal_dict
    
    Input: document (str), removal dict(items: old_string, values: replacement_string)
    
    Output: replacement_document(str)"""
    replacement_document = document
    print(removal_dict)

    for key, value in removal_dict.items():
        pattern = r"\b" + re.escape(key) + r"\b"
        replacement_document = re.sub(pattern, "", replacement_document)
    return replacement_document



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text", required=True, help="Name of the text in the texts_folder"
    )
    args = parser.parse_args()
    lemmatizer = WordNetLemmatizer()

    with open(f"../texts/{args.text}.txt", "r") as f:
        text = f.read()

    c1_vocab = pd.read_csv("octanove-vocabulary-profile-c1c2-1.0.csv")
    simple_vocab_list = pd.read_csv("cefrj-vocabulary-profile-1.5.csv")
    b2_vocab = simple_vocab_list[simple_vocab_list["CEFR"] == "B2"]["headword"]

    # word lists gotten from https://raw.githubusercontent.com/openlanguageprofiles/olp-en-cefrj/refs/heads/master/cefrj-vocabulary-profile-1.5.csv
    # https://github.com/openlanguageprofiles/olp-en-cefrj

    complex_word_list = list(c1_vocab["headword"])
    complex_word_list.extend(list(b2_vocab))

    nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer", "textcat"])
    matcher = Matcher(nlp.vocab)

    # nlp.add_pipe(
    #     "spacy_chunks",
    #     last=True,
    #     config={
    #         "chunking_method": "sentence",
    #         "chunk_size": 10,
    #         "overlap": 1,
    #         "truncate": True,
    #     },
    # )

    doc = nlp(text)


    dict_adjectives = find_adjectives_before_nouns(doc)
    list_adverbs = find_adverbs(doc)

    replacement_doc = replace_words(doc.text, dict_adjectives)
    replacement_doc = replace_words(replacement_doc, list_adverbs)
    breakpoint()

    new_document = nlp(replacement_doc)
    hypernym_doc = replace_with_hypernym(complex_word_list, new_document)



    breakpoint()


    with open(f"../texts/{args.text}_simplified.txt", "w") as t:
        t.write(hypernym_doc)

    # wordnet_dict = wordnet_tokenization(text)
