# ParaphrasesAPI
Finds in the text all Noun Phrases ('NP' tag) - noun phrases consisting of Several NPs separated by comma or conjunctive inflection and generates variants of transposed places of these child NPs with each other.

## Launch
Clone repository:

```
git clone https://github.com/ejenliya/ParaphrasesAPI
```

Create and activate virtual environment in the folder:

```
virtualenv venv
source venv/bin/activate
```

Install requirements from requirements.txt:

```
pip install -r requirements.txt
```

Next run the server:

```
uvicorn main:app --reload
```

Go to the http://localhost:{port}/docs. Here you can see created API and test it.
Or use a link like: http://localhost:{port}/paraphrase?tree={string_representation_of_syntactic_tree}