import argparse
import os
import re

from tqdm.auto import tqdm


def delete_beginning(text):
    """Deletes the additional information text at the beginning provided by gutenberg.org"""
    beginning_text_index = text.index(
        [i for i in text if re.findall(r"\*\*\* START OF THE PROJECT GUTENBERG", i)][0]
    )
    text_cleared_beg = text[beginning_text_index + 1 :]
    return text_cleared_beg


def delete_end(text):
    """Deletes the additional information text at the end provided by gutenberg.org"""
    end_text_index = text.index(
        [i for i in text if re.findall(r"\*\*\* END OF THE PROJECT GUTENBERG", i)][0]
    )
    text_cleared_end = text[:end_text_index]
    return text_cleared_end


# remove emtpy lines too?
def remove_empty_spaces(text_lines):
    stripped_lines = [line.strip() for line in text_lines]
    cleaned_lines = [line for line in stripped_lines if len(line) != 0]
    return cleaned_lines


def remove_newlines(text_lines):
    fulltext = " ".join(text_lines)
    sentences = fulltext.split(".")
    cleaned_sentences = [sentence.replace("\n", " ") for sentence in sentences]
    dotted_sentences = [sentence + "." for sentence in cleaned_sentences]
    dotted_sentences = dotted_sentences[:-1]
    return dotted_sentences


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        required=False,
        help="Input is the title of the text in the text folder, default is all in the folder",
        default="all"
    )
    args = parser.parse_args()

    if args.text == "all":
        texts = os.listdir("text/raw")
    else:
        texts = args.text.split()

    for text in tqdm(texts):
        # if "by" not in text:
        #     title = "Unknown"
        # else:
        #     title = text.split("by")[0].strip()
        with open(f"text/raw/{text}", "r") as f:
            text_lines = f.readlines()

        cleaned_lines = remove_empty_spaces(text_lines)
        beg_text = delete_beginning(cleaned_lines)
        clean_text = delete_end(beg_text)
        clean_text = remove_newlines(clean_text)
        short_text = clean_text[100:300]

        preprocessed_path = "text/preprocessed"
        if not os.path.isdir(preprocessed_path):
            os.makedirs(preprocessed_path)

        with open(f"text/preprocessed/{text.split(".txt")[0]}.txt", "w") as f:
            f.writelines(short_text)
