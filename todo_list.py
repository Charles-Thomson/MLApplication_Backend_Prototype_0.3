# TODO NEXT

# Test out Marshal to see if it can be used to turn the brain instance functions into/ out of JSON
# this will then remove the need to have function refs - can just have callable
# only need to be assigned once at point of creation - not on rebuild


# Start testing the DB elements inc:
# Saving to the DB
# Getting from the DB and changing back to a Brain Instance

# model_data_formatting is messy and needs to be refactored down

# Look into refactoring model_to_brain_instance using a serializer
# Removes the creation of the dict

# Can a function be given to to the models.Model and then called by said model
# i.e don't save the activation ect functions to a field ?


# Handling of the current_generation var for each instance
# This is now stored in the config fo each instance

# Write tests for the new setting of the brain_config/ann_config
# Also fix the naming of this var as it is confusing
