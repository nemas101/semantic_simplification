import argparse
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
    stripped_lines = [line.strip() for line in tqdm(text_lines)]
    cleaned_lines = [line for line in tqdm(stripped_lines) if len(line) != 0]

    return cleaned_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text", required=True, help="Name of the text in the texts_folder"
    )
    args = parser.parse_args()

    with open(f"../texts/{args.text}.txt", "r") as f:
        text = f.readlines()
    cleaned_lines = remove_empty_spaces(text)
    beg_text = delete_beginning(cleaned_lines)
    clean_text = delete_end(beg_text)

    with open(f"../texts/{args.text}_preprocessed.txt", "w") as f:
        f.writelines(line + "\n" for line in clean_text)
