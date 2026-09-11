"""Creates a file with all readability scores of the project
Inputs are the original and the preprocessed texts
Output is a json file with the readability (and embedding) scores
"""

import argparse
import os

import numpy as np
import pandas as pd
import spacy
import textstat
from tqdm import tqdm


def scoring_embedding(text: str) -> float:
    """Scores the mean of semantic embedding from spacy.

    Input: text(str)
    Outputs: list of the means of the distance between
        1. all vectors (float)
        2. vectors of tokens consisting only of alphabetic characters (float)
        3. all vectors excluding stop words, punctucation and whitespaces (float)"""

    nlp = spacy.load("en_core_web_lg", disable=["ner", "lemmatizer", "textcat"])

    parsed_text = nlp(text)
    # filter out everything that is not alphabetical and all stop words
    vectors = [token.vector for token in parsed_text]
    mean_simple = np.average(vectors)
    filtered_all = [
        token for token in parsed_text if token.is_alpha and not token.is_stop
    ]
    vectors_all_filters = [token.vector for token in filtered_all]
    mean_all_filters = np.average(vectors_all_filters)
    filtered_stop_punct = [
        token
        for token in parsed_text
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    vectors_stop_punct = [token.vector for token in filtered_stop_punct]
    mean_filtered = np.average(vectors_stop_punct)
    scores = {}
    scores["mean_simple"] = mean_simple
    scores["mean_alpha"] = mean_all_filters
    scores["mean_filtered"] = mean_filtered
    return scores


def scoring_readability(text: str) -> dict:
    """ "Scores the readability scores for text:

    Input: Text (str)
    Output: Dictionary with the scores in the form
            {"Test_name": value}"""

    tests = [
        textstat.flesch_reading_ease,
        textstat.flesch_kincaid_grade,
        textstat.smog_index,
        textstat.coleman_liau_index,
        textstat.automated_readability_index,
        textstat.dale_chall_readability_score,
    ]
    red_scores = {}
    for red_test in tests:
        red_scores[red_test.__name__] = red_test(text)
    return red_scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        required=False,
        help="Give name of the title in the text folder, defaults to all in the text folder",
        default="all",
    )
    parser.add_argument(
        "--method",
        required=False,
        help="Choose scoring methods for text from [readability, semantic_embedding, all],  default is all",
        default="all",
    )
    args = parser.parse_args()

    if args.text == "all":
        texts = os.listdir("text/raw")
    else:
        texts = args.text.split()

    raw_texts = []
    new_texts = []
    titles = []
    # mean_simple_list = []
    # mean_alpha_list = []
    # mean_filtered_list = []
    # new_mean_simple_list = []
    # new_mean_alpha_list = []
    # new_mean_filtered_list = []
    # embedding_dict = {
    #     "mean_simple": mean_simple_list,
    #     "mean_alpha": mean_alpha_list,
    #     "mean_filtered": mean_filtered_list,
    #     "mean_simple_new": new_mean_simple_list,
    #     "mean_alpha_new": new_mean_alpha_list,
    #     "mean_filtered_ew": new_mean_filtered_list,
    # }
    dict_list = []

    for text in tqdm(texts):
        title = text.split(".txt")[0]
        titles.append(title)
        with open(f"text/preprocessed/{text}", "r") as f:
            original_text = f.read()
            raw_texts.append(original_text)

        with open(f"results/text/{title}-simplified.txt", "r") as f:
            simplified_text = f.read()
            new_texts.append(simplified_text)

        score_dict = {}
        score_dict["original_text"] = original_text
        score_dict["simplified_text"] = simplified_text

        #readability
        readability_scores_old = scoring_readability(original_text)
        readability_scores_new = scoring_readability(simplified_text)
        new_readability_scores = [
            "flesch_reading_ease_new",
            "flesch_kincaid_grade_new",
            "smog_index_new",
            "coleman_liau_index_new",
            "automated_readability_index_new",
            "dale_chall_readability_score_new",
        ]

        readability_scores_new = dict(zip(new_readability_scores, list(readability_scores_new.values())))
        score_dict.update(readability_scores_old)
        score_dict.update(readability_scores_new)

        # embedding
        embeddings_old = scoring_embedding(original_text)
        embeddings_new = scoring_embedding(simplified_text)
        new_embedding_scores = [
            "mean_simple_new",
            "mean_alpha_new",
            "mean_filtered_new",
        ]
        embeddings_new = dict(zip(new_embedding_scores, list(embeddings_new.values())))
        score_dict.update(embeddings_old)
        score_dict.update(embeddings_new)

        dict_list.append(score_dict)

    df = pd.DataFrame(dict_list)
    df.to_json("results/results.json")
