# TODO Today:
# Logging
# DONE 1. Function logging
# Logger to wrap the Learning instance- run_instance function
# Logger to wrap the learning_instance - run_generation function
# Both go to the same log file and show the start and end time of each learning_instance/ generation

# DONE 2. Function logging
# Wapper for run_generation_instance
# Logging all the brain instances
# Logging all the fit brain instaces

# Done 3. Logging for fitness avergae
# Want the generation number and average fitness in the log

# 4. Write a test for a full - longer length run of the system
# Setting of the alpha brain
# If the threshold stops new generation, the alpha brain is of the old generation
# Need a way to get the data from the generation even if it fails and be able to store it

# 5. have the logs create a new folder to add logs to per run


# Look into how to properly use the get.loger functions
# Wrapper on the run_generation function
# logging of the average fitness per generation
# logging of the brain instance_paths and the related fitness's
# - by generation and instance

# Can some of the data_modeling/interal_functions be refacroted down ? - can change the function to get

# data back from Learning instance and generational mdodels to use a factory on the serializers ?

# Is the generation id the same as the DB ref for the data base ??

# Naming convention across the files need to be fixed , generation_db_ref to generation instance ref ect is bad

# Fix views side of the DB
# add generation_number to the brain instance model
