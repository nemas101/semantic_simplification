from tqdm.auto import tqdm
import argparse

def delete_beginning(text):
    beginning_text = text.index("*** START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS ***")
    text_cleared_beg = text[beginning_text+1:]
    return text_cleared_beg

def delete_end(text):
    end_text = text.index("*** END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS ***")
    text_cleared_end = text[:end_text]
    return text_cleared_end

# remove emtpy lines too?
def remove_empty_spaces(text_lines):
    stripped_lines = [line.strip() for line in tqdm(text_lines)]
    cleaned_lines = [line for line in tqdm(stripped_lines) if len(line) != 0]

    return cleaned_lines

if __name__ == "__main__":
    with open("../texts/frankenstein_shelley.txt", "r") as f:
        text = f.readlines()
    cleaned_lines = remove_empty_spaces(text)
    beg_text = delete_beginning(cleaned_lines)
    clean_text = delete_end(beg_text)

    with open("../texts/frankenstein_shelley_preprocessed.txt", "w") as f:
        f.writelines(line + '\n' for line in clean_text)

