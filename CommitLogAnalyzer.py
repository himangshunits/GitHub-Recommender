'''This file contains the code for analyzing and scoring 5 different aspects of the github commit logs
We check to see the inclination or seriousness of the user towards a particular commit log message, or a bunch of commit log messsages uasing the
following philosophy.'''
# Length of the log after pre-processing
# Structural integrity/Grammatical integrity
# Does topic match with description.
# How positive was the sentiment
# How many spelling errors?


import graphlab as gl
from PreprocessManager import PreprocessManager
from fuzzywuzzy import fuzz
import grammar_check as gc
from enchant.checker import SpellChecker



class CommitLogAnalyzer:

    def __init__(self):
        self.grammar_tool = gc.LanguageTool('en-GB')
        self.spell_master = SpellChecker("en_US")
        self.senti_checker = gl.sentiment_analysis.create()



    def process_one_log(self, input_log, repo_info_topics):
        # Find the length
        length = len(PreprocessManager.get_unique_words(input_log))

        # Find structural integrity.
        self.grammar_tool.enable_spellchecking()
        problematic_matches = self.grammar_tool.check(input_log)
        corrected_text = gc.correct(input_log, problematic_matches)
        degree_of_mismatch = 100 - fuzz.ratio(input_log, corrected_text)
        structural_integrity_score = degree_of_mismatch * len(problematic_matches)

        # Check if topic is relevant
        # This is still in testing phase and not sure if it has a good impact on the final results.
        # Might be totally useless at times.
        sframe_data_for_topics = gl.SArray([PreprocessManager.get_word_counts(input_log)])
        # Add Associations here TODO
        topic_model = gl.topic_model.create(sframe_data_for_topics)
        pred = topic_model.predict(sframe_data_for_topics, output_type='probability')
        topics = topic_model.get_topics(output_type='topic_words')

        print pred
        print topics




        # Check how much positivity
        log_dict = dict()
        log_dict['text'] = input_log
        positivity = self.senti_checker.predict_row(log_dict)
        positivity_ranking = 100 * positivity

        print positivity_ranking





        # Spelling Goodness
        self.spell_master.set_text(input_log)
        error_words = list()
        for err in self.spell_master:
            error_words.append(err.word)
        spelling_intigrity_score = len(error_words)

    def process_batch_logs(self, input_log_collection, repo_info):
        # Call process_one and normalize by no. of data points
        pass



