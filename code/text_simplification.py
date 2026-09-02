import argparse
import re
import os

import pandas as pd
import spacy
from nltk.corpus import stopwords
from spacy.matcher import Matcher
from tqdm.auto import tqdm
from hypernymReplacement import replace_with_hypernym
# if necessary run there once:
# nltk.download('stopwords')
# nltk.download("punkt_tab")
# nltk.download("wordnet")


def spacyfy_text(text: str) -> list[str]:
    n = 99999  # set for spacys maximal text limit
    chunks = [text[i : i + n] for i in range(0, len(text), n)]
    sentences = []
    for chunk in tqdm(chunks):
        chunk_spacyfied = [sentence for sentence in nlp(chunk).sents]
        sentences.extend([sentence.text for sentence in chunk_spacyfied])

    return sentences


def find_adjectives_before_nouns(document: spacy.tokens.doc.Doc) -> dict:
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
            filtered_adj_matches[document[start:end].text] = document[
                start + 1 : end
            ].text
        prev_match = (match_id, start, end)

    matcher.remove("adj_noun")  # matches all adj-noun combinations
    matcher.remove("only_adj")

    return filtered_adj_matches


def find_adverbs(document: spacy.tokens.doc.Doc) -> dict:
    """
    Finds any adverbs in a given document
    Adverbs are then filtered by the stopword-list from spacy because too many "adverbs" are prepositions

    Input: spacy-document of the text (spacy.tokens.doc.Doc')

    Output: list of of the adverbs to be replaces (list of str)
    """
    pattern_adv = [[{"POS": "ADV"}]]

    matcher.add("adv", pattern_adv)  # matches all adverbs

    matches = matcher(document)

    stops = set(stopwords.words("english"))
    filtered_adv_matches = {}

    for _, start, end in matches:
        filtered_adv_matches[document[start:end].text] = ""
    filtered_adv_matches_without_stops = {
        item: value for item, value in filtered_adv_matches.items() if item not in stops
    }
    return filtered_adv_matches_without_stops


def replace_words(document: str, removal_dict: dict) -> str:
    """Replaces words in a document according to a given removal_dict

    Input: document (str), removal dict(items: old_string, values: replacement_string)

    Output: replacement_document(str)"""
    replacement_document = document
    # print(removal_dict) # for testing purposes
    for key, value in removal_dict.items():
        pattern = r"\b" + re.escape(key) + r"\b"
        replacement_document = re.sub(pattern, value, replacement_document)
    return replacement_document


def clean_document(text: str) -> str:
    single_whitespaces = re.sub(r" {2,}", " ", text)
    fullstop_replacement = re.sub(
        r"(( )*(\.) )+", ". ", single_whitespaces
    )  # remove whitespaces around full stops
    comma_replacement = re.sub(
        r"(( )*(,) )+", ", ", fullstop_replacement
    )  # remove doubled commas and superfluous whitespaces
    return comma_replacement


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        required=False,
        help="Give name of the title in the text folder, defaults to all in the text folder",
        default="all"

    )
    args = parser.parse_args()

    if args.text == "all":
        texts = os.listdir("text/preprocessed")
    else:
        texts = args.text.split()

    c1_vocab = pd.read_csv("code/octanove-vocabulary-profile-c1c2-1.0.csv")
    simple_vocab_list = pd.read_csv("code/cefrj-vocabulary-profile-1.5.csv")
    b2_vocab = simple_vocab_list[simple_vocab_list["CEFR"] == "B2"]["headword"]

    # word lists gotten from https://raw.githubusercontent.com/openlanguageprofiles/olp-en-cefrj/refs/heads/master/cefrj-vocabulary-profile-1.5.csv
    # https://github.com/openlanguageprofiles/olp-en-cefrj
    complex_word_list = list(c1_vocab["headword"])
    complex_word_list.extend(list(b2_vocab))

    nlp = spacy.load("en_core_web_md", disable=["ner", "lemmatizer", "textcat"])
    matcher = Matcher(nlp.vocab)

    for text in tqdm(texts):
        with open(f"text/preprocessed/{text}", "r") as f:
            text = f.read()


        doc = nlp(text)

        breakpoint()
        # TODO HIER weitermachen

        dict_adjectives = find_adjectives_before_nouns(doc)
        list_adverbs = find_adverbs(doc)

        # remove adjectives and adverbs
        replacement_doc = replace_words(doc.text, dict_adjectives)
        replacement_doc = replace_words(replacement_doc, list_adverbs)
        # replace complex words
        new_document = nlp(replacement_doc)
        hypernym_doc = replace_with_hypernym(complex_word_list, new_document)
        # clean document
        clean_document = clean_document(hypernym_doc)

        results_path = "/results"
        if not os.path.isdir(results_path):
            os.makedirs(results_path)

        with open(f"results/{text.split(".txt")[0]}-simplified.txt", "w") as t:
            t.write(clean_document)
