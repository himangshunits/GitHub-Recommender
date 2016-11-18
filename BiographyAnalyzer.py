# This class processes the BIO texts and looks for fuzzy matches for the following 5 kind of keywords in the text.
# interests, technologies, languages, position, student_status
# The all 5 kind of things has a tolerance associated with them, which must be specified at the time of object creation.

from fuzzywuzzy import fuzz
from PreprocessManager import PreprocessManager
import itertools as itr
import unicodedata
import ConfigurationManager as cfg



class BiographyAnalyzer:

    def __init__(self, interests_tolerance, tech_tolerance, languages_tolerance, position_tolerance, student_status_tolerance):
        self.interests_tolerance = interests_tolerance
        self.tech_tolerance = tech_tolerance
        self.languages_tolerance = languages_tolerance
        self.position_tolernce = position_tolerance
        self.student_status_tolerance = student_status_tolerance
        # Create lists for the reference dictionaries. Kept as list because of fuzzy matching
        self.interest_dict = list()
        self.tech_dict = list()
        self.lagunages_dict = list()
        self.position_dict = list()
        self.student_status_dict = list()
        self.__init_dicts__()



    def get_data_from_file(self, path):
        result = list()
        try:
            f = open(path, 'r')
            data = f.read()
            result = data.split('\n')
        except IOError as e:
            print "Error in file opening = " + path
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return result



    # Finds the matches from input with corpus data. If the match crosses tolerance, record that pair. Return the running highest pair
    def get_best_match(self, input, corpus, tolerance):
        cartesian = itr.product(input, corpus)
        max_match = 0
        max_p = ""
        max_q = ""
        for p, q in cartesian:
            match_percentage = fuzz.ratio(p, q)
            if(match_percentage > max_match):
                max_match = match_percentage
                max_p = p
                max_q = q
        return max_p, max_q



    def __init_dicts__(self):
        self.interest_dict = self.get_data_from_file(cfg.interests_file)
        self.lagunages_dict = self.get_data_from_file(cfg.language_file)
        self.position_dict = self.get_data_from_file(cfg.position_file)
        self.student_status_dict = self.get_data_from_file(cfg.student_status_file)
        self.tech_dict = self.get_data_from_file(cfg.tech_file)





    # Processes the bio text and finds the categories from the dictionaries
    def process_bio(self, input_bio):
        # Convert to ord()
        bio_data = PreprocessManager.get_unique_words(input_bio)
        bio_data = [str(word) for word in bio_data]
        # Match interests
        [interest_p, interest_q] = self.get_best_match(bio_data, self.interest_dict, self.interests_tolerance)

        # Match technologies
        [tech_p, tech_q] = self.get_best_match(bio_data, self.tech_dict, self.tech_tolerance)


        # Match languages
        [languages_p, languages_q] = self.get_best_match(bio_data, self.lagunages_dict, self.languages_tolerance)

        # Match positions
        [positions_p, positions_q] = self.get_best_match(bio_data, self.position_dict, self.position_tolernce)


        # Match Student Statutes
        [status_p, status_q] = self.get_best_match(bio_data, self.student_status_dict, self.student_status_tolerance)

        return interest_q, tech_q, languages_q, positions_q, status_q


