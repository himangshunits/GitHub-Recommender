import ConfigurationManager as cfg




def add_log_to_file(string_data, filename = cfg.log_file_path):
    file = open(filename, "a")
    file.write(string_data)
    file.write("\n")
    file.write("##########################################################################################################################################")
    file.write("##########################################################################################################################################")
    file.write("##########################################################################################################################################")
    file.write("\n")
    file.close()