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
        input_log = PreprocessManager.remove_non_ascii(input_log)
        # TODO : Do we need repo info?
        #repo_info_topics = PreprocessManager.remove_non_ascii(repo_info_topics)
        # Find the length
        # TODO : All the scores which are dependent on the length are not unbiased if not normalized! Check that
        length = len(PreprocessManager.get_raw_tokenized_text(input_log))

        # Find structural integrity.
        self.grammar_tool.enable_spellchecking()
        problematic_matches = self.grammar_tool.check(input_log)
        corrected_text = gc.correct(input_log, problematic_matches)
        degree_of_match = fuzz.ratio(input_log, corrected_text)
        structural_integrity_score = degree_of_match * (length - len(problematic_matches))

        # Check if topic is relevant
        # This is still in testing phase and not sure if it has a good impact on the final results.
        # Might be totally useless at times.
        sframe_data_for_topics = gl.SArray([PreprocessManager.get_word_counts(input_log)])
        # Add Associations here TODO: Make it proper
        associations = gl.SFrame({'word': ['fix', 'issue', 'implement', 'modify', 'changed', 'bug', 'error'],
                               'topic': [0, 0, 0, 0, 0, 0, 0]})

        topic_model = gl.topic_model.create(sframe_data_for_topics, associations=associations)

        # TODO : Add here the match with the description. Is that useful? Maybe Future work?

        #pred = topic_model.predict(sframe_data_for_topics, output_type='probability')
        topics = topic_model.get_topics()
        # The final score is the sum of all the topic 0 scores! As they were used in associations. Gives us relevance of being a commit message!
        topic_relevance_score = 0
        for i in xrange(0, len(topics)):
            curr = topics[i]
            topic_id = curr['topic']
            score_val = curr['score']
            if topic_id == 0:
                topic_relevance_score += score_val

        topic_relevance_score *= 100

        #print topics, topic_relevance_score



        # Check how much positivity
        log_dict = dict()
        log_dict['text'] = input_log
        positivity = self.senti_checker.predict_row(log_dict)
        positivity_score = 100 * positivity

        #print positivity_score




        # Spelling Goodness
        self.spell_master.set_text(input_log)
        error_words = list()
        for err in self.spell_master:
            error_words.append(err.word)
        spelling_integrity_score = length - len(error_words)


        #return all
        return length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score

    def process_batch_logs(self, input_log_collection, repo_info):
        # Call process_one and normalize by no. of data points
        size_of_collection = len(input_log_collection)
        # length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score
        length_total = 0
        structural_integrity_score_total = 0
        topic_relevance_score_total = 0
        positivity_score_total = 0
        spelling_integrity_score_total = 0
        print "The size of the batch = " + str(size_of_collection)

        for log in input_log_collection:
            print "Processing the log = " + str(log)
            [length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score] \
                = self.process_one_log(log, repo_info)
            length_total += length
            structural_integrity_score_total += structural_integrity_score
            topic_relevance_score_total += topic_relevance_score
            positivity_score_total += positivity_score
            spelling_integrity_score_total += spelling_integrity_score

        return length_total/(size_of_collection + 1), structural_integrity_score_total/(size_of_collection + 1), topic_relevance_score_total/(size_of_collection + 1), \
               positivity_score_total/(size_of_collection + 1), spelling_integrity_score_total/(size_of_collection + 1)



