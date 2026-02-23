import re

def delete_beginning(text):
    beginning_text = r".*(\*\*\* START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS \*\*\*)"

    text_cleared_beg = re.sub(beginning_text, "", text)
    return text_cleared_beg

def delete_end(text):
    end_text = r"(\*\*\* END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS \*\*\*).*"
    text_cleaned_fully = re.sub(end_text, "", text)
    return text_cleaned_fully

# remove emtpy lines too?
def remove_empty_spaces(text_lines):
    stripped_lines = [line.strip() for line in text_lines]
    cleaned_lines = [line for line in stripped_lines if len(line) != 0]

    return cleaned_lines

if __name__ == "__main__":
    with open("../texts/frankenstein_shelley.txt", "r") as f:
        text = f.readlines()
        cleaned_lines = remove_empty_spaces(text)
        text = " ".join(cleaned_lines)
        beg_text = delete_beginning(text)
        breakpoint()
        clean_text = delete_end(beg_text)
        breakpoint()

