# TODO Today;
# DONE 1. Refactor the file format for the model data formatting into data_modeling folder that splits into the modeling fr each of the models
# DONE 2. Test file - the tests for saving and getting the generation models + alterations based on refactoring
# DONE 3. The functions for the saving and getting of a brain instance
# DONE 4. the tests for the saving and the getting of brain instances
# 5. Implementing the new model structure into the main system
# step 1 - save the learning instance and pass the ref to the generation
# step 2 - save the generation and pass the ref down to the saving of each brain - in run_generation
# *** GOT THIS FAR ***
# step 3 - on completion of generation - update generation model data
# step 4 - update learning instance model data

# TODO NEXT:
# Write the functions for updatting the learning instance and Generation models
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
