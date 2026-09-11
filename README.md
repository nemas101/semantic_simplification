# semantic_simplification

### 1. Download data
Download the data from gutenberg.org via `download_gutenberg.py`. If run with no arguments it will download a list of 100 books from the gutenberg top 100 engisch book list (list assembled at 14.07.25).

 Example: ```uv run python code/download_gutenberg.py```

 time: ~ 4 min

### 2. Preprocess 
Preprocess the books via `preprocessing.py` script.

 Example: ```uv run python code/preprocessing.py```

 time: ~ < 1 min

### 3. Text Simplification
Run the text simplification including 

 Example: ```uv run python code/text_simplification.py```

 time ~ 3 min

### 4. Readability Scores
Compute the different readability scores

 Example: ```uv run python code/readability_scores.py```

 time: ~8 min

 ### 5. Data Exploration

 Using the jupyter notebook `data_exploration.ipynb` in `/code/visualisation`, plots for a comparison of readability scores and embedding scores can be generated.