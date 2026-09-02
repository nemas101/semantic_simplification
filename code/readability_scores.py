import argparse
import os

import pandas as pd
import textstat


def scoring_readability(original_text, preprocessed_text):
    scoring_scores = {
        "flesch_reading_ease": [],
        "flesch_kincaid_grade": [],
        "smog_index": [],
        "coleman_liau_index": [],
        "automated_readability_index": [],
        "dale_chall_readability_score": [],
    }

    # original text
    scoring_scores["flesch_reading_ease"].append(
        textstat.flesch_reading_ease(original_text)
    )
    scoring_scores["flesch_kincaid_grade"].append(
        textstat.flesch_kincaid_grade(original_text)
    )
    scoring_scores["smog_index"].append(textstat.smog_index(original_text))
    scoring_scores["coleman_liau_index"].append(
        textstat.coleman_liau_index(original_text)
    )
    scoring_scores["automated_readability_index"].append(
        textstat.automated_readability_index(original_text)
    )
    scoring_scores["dale_chall_readability_score"].append(
        textstat.dale_chall_readability_score(original_text)
    )

    # preprocessed text
    scoring_scores["flesch_reading_ease"].append(
        textstat.flesch_reading_ease(preprocessed_text)
    )
    scoring_scores["flesch_kincaid_grade"].append(
        textstat.flesch_kincaid_grade(preprocessed_text)
    )
    scoring_scores["smog_index"].append(textstat.smog_index(preprocessed_text))
    scoring_scores["coleman_liau_index"].append(
        textstat.coleman_liau_index(preprocessed_text)
    )
    scoring_scores["automated_readability_index"].append(
        textstat.automated_readability_index(preprocessed_text)
    )
    scoring_scores["dale_chall_readability_score"].append(
        textstat.dale_chall_readability_score(preprocessed_text)
    )

    return scoring_scores


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
        texts = os.listdir("../text/raw")
    else:
        texts = args.text.split()

    with open(f"text/{args.text}_prep.txt", "r") as f:
        original_text = f.read()

    with open(f"text/{args.text}_prep_simplified.txt", "r") as f:
        preprocessed_text = f.read()

    scores = scoring_readability(original_text, preprocessed_text)
    df_read_scores = pd.DataFrame.from_dict(scores, orient="index", columns=["preprocessed text", "simplified text"])

    print(df_read_scores)
    breakpoint()
