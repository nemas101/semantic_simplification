import spacy
import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
# nltk.download("punkt_tab")
nltk.download("wordnet")
from tqdm.auto import tqdm



def spacyfy_text(text) -> list[str]:
    n = 99999  # set for spacys maximal text limit
    chunks = [
        text[i : i + n]
        for i in range(0, len(text), n)
    ]
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

if __name__ == "__main__":
    with open ("../texts/frankenstein_shelley.txt", "r") as f:
        text = f.read()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    wordnet_dict = wordnet_tokenization(text)

    breakpoint()
    # spacy_fy_sentences = spacyfy_text(text)