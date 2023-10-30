# TODO Today:

# DONE 1. Look at refacoting down the loging decorators
# can create the deocs at the run_instance deco, return a generator for each that can then be passed to the next deco ?
# Finally worked this out with **kwargs !!


# 1.1 Fix tests from refactoring

# 2. Refactoring down the Instance_generation file
# - Move the instance into a new folder ?
# - move data config to it's own folder ?

# 3. Look at Azure DB options to intergrate


# The logging decos need to be refactored down
# see if all the additional var passing can be reduced ?


# Look at GQL layer over API ?

# Add the debug logger into the logging files

# 2. Stat refactoring down the instance_generation file
# Look into the ID system all the way down - it,s not very descriptive of cohesive currently


# 3. refactor down other files where possible

# 4. move onto the views file
# Work out the return data structure thats needed
# write the functions to get the relervent data from th DB and fromat


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
