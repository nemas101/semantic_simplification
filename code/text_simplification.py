import argparse
import pandas as pd
import nltk
import spacy
from nltk import word_tokenize
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


def wordnet_tokenization(text):
    wordnet_tokens = {}
    nltk_words = word_tokenize(text)
    for word in tqdm(nltk_words):
        wordnet_tokens[word] = wn.synsets(word)
    return wordnet_tokens


def replace_with_hypernym(vocab_list, document):
    """Replaces 'complex' words (defined as words from the C1/C2 readers level from CEFR-J) with their first hypernyms from wordnet"""
    word_list = [w.text for w in document]
    # maybe lemmatize for all the verbs?
    # lemma_list = [lemmatizer.lemmatize(word) for word in word_list]
    for index, word in enumerate(word_list):
        lemma = lemmatizer.lemmatize(word)
        if lemma in vocab_list:
            synset = wn.synsets(word)
            if len(synset) > 0:
                hypernym_list = synset[0].hypernyms()
                if len(hypernym_list) > 0:
                    hypernym = hypernym_list[0]
                    word_hypernym_synset = hypernym
                    name = word_hypernym_synset.name()
                    new_word = name.split(".")[0]
                    word_list[index] = new_word    
    document = " ".join(word_list)
    return document


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text", required=True, help="Name of the text in the texts_folder"
    )
    args = parser.parse_args()
    lemmatizer = WordNetLemmatizer()

    with open(f"../texts/{args.text}.txt", "r") as f:
        text = f.read()
    df_vocab = pd.read_csv("c1c2_vocab_list.csv")
    complex_word_list = list(df_vocab["headword"])

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    spacy_fy_sentences = spacyfy_text(text)

    hypernym_doc = replace_with_hypernym(complex_word_list, doc)
    breakpoint()
    # wordnet_dict = wordnet_tokenization(text)

