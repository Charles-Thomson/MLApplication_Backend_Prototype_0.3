# TODO Today:
# Fix the tests
# Move onto the logging side of things


# Logging
# Look into how to properly use the get.loger functions
# Wrapper on the run_generation function
# logging of the average fitness per generation
# logging of the brain instance_paths and the related fitness's
# - by generation and instance

# TODO NEXT:
# The process of generation_model creation/savin/ updating is messy and needs to be refactored

# Can some of the data_modeling/interal_functions be refacroted down ? - can change the function to get
# data back from Learning instance and generational mdodels to use a factory on the serializers ?

# Is the generation id the same as the DB ref for the data base ??

# Look for the best approach for the saving of the brain instances  - one at a time or as a whole generaiton
# Think about if the learning instance and generation objects are needed ?

# Logging for each of the model save points in the main system

# Naming convention across the files need to be fixed , generation_db_ref to generation instance ref ect is bad

# Fix views side of the DB
# add generation_number to the brain instance model
