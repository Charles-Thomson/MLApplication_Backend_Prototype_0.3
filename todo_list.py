# TODO NEXT

# Currently in the testing django file - working on the test to save and et back generation objects using the fk aproach

# 1. getting the saved generation_models back from the db via the use of the learning instance fk/pk

# 2. Do the same test but from brain isnaces
# Make a learing instance -> geneartion insatnce -> BrainInstance
# Get all the brain instances back via the generational_object fk ect


# Instance -> generation -> Brains


# FIX LIST
# 1. The current process of data formatitng is very messy and unclear
# Refactor down this approach and try to clarify using function names


# Add the passing of var data to the views - then add this to the testing

# Work out the ID system - final brain instance needs to be linked to each of the saved generations
# Or create an over arching model for each the inc the final brain and generation based data ?


# Add the var path to the URLS for the views - i.e the brain instance to be saved ect

# add generation_number to the brain instance model

# IDEAS

# Serialize/ picklejson the whole brain instance - just keep out the vars that want to be searchable
