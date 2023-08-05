"""
Suggest Analyzer and Auto Complete Filter Class
"""
from elasticsearch_dsl import analyzer, token_filter

other_param = dict()


class Suggest(object):
    other_param.update({"min_gram": 1, "max_gram": 20})

    @staticmethod
    def suggest():
        suggestfilter = token_filter("suggestfilter", type="ngram",
                                     **other_param)

        bestsuggest = analyzer("bestsuggest", tokenizer="standard",
                               filter=["lowercase", suggestfilter,
                                       "asciifolding"])
        return bestsuggest

    @staticmethod
    def autocomplete():
        autocompletefilter = token_filter("autocompletefilter",
                                          type="edge_ngram", **other_param)
        autocomplete = analyzer("autocomplete", tokenizer="standard",
                                filter=["lowercase", autocompletefilter])
        return autocomplete

