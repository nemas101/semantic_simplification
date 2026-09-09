# semantic_simplification

### 1. Download data
Download the data from gutenberg.org via `download_gutenberg.py`. If run with no arguments it will download a list of 100 books from the gutenberg top 100 engisch book list (list assembled at 14.07.25).

 Example: ```uv run python code/download_gutenberg.py```

### 2. Preprocess 
Preprocess the books via `preprocessing.py` script.

 Example: ```uv run python code/preprocessing.py```

### 3. Text Simplification
Run the text simplification including 

 Example: ```uv run python code/text_simplification.py```

### 4. Readability Scores
Compute the different readability scores

 Example: ```uv run python code/readability_scores.py```