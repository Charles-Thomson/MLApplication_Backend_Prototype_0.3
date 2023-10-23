# TODO Today;
# 1. Remove the generation_instance_object - refactor down to work the same as the learning instance_save()
# 2. Write tests for the updating of data for the generation and Learning instace models
# 3. Clean up the instance_generation_main
# - Currently very messy
# Need to work out alpha_brain
# Clean up the run generation
# clean up th new fitness threshold/ avg_fitness


# TODO NEXT:
# The generation object can be removed - only need an ID at the point of creation in the same form as the Learning instance
# Only passing in the generation ID - which is then saved to be used in the update

# The process of generation_model creation/savin/ updating is messy and needs to be refactored

# Is the generation id the same as the DB ref for the data base ??

# Look for the best approach for the saving of the brain instances  - one at a time or as a whole generaiton
# Think about if the learning instance and generation objects are needed ?

# Is it worth moving away from the storage objects for each learning/generation - will they ever be used ?

# 6. Logging for each of the model save points in the main system

# Naming convention across the files need to be fixed , generation_db_ref to generation instance ref ect is bad

# Future work
# Can the leraning instance/ generation refs for the DB be stored on the application side
# Can be created a the point of generation/brain creation

# Fix views side of the DB
# add generation_number to the brain instance model
