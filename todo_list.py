# TODO NEXT

# TodoList for the day
# Enter the django module settings
# last working on: loggig file refacotring and implementation


# DONE 1. Clean up the adding/getting and formatting of database models - it's messey currently
# DONE 2. Layout and usage of the fomatting of the data_to_model ect needs to be refactored down/ cleaned up
# DONE 3. can unessesary function calls be removed from the adding of generations - currently have a middle man style thing going on
# DONE 4.  ID system for each leaning instance - this will be passed to each brain instance and each generation_model

# DONE 5. Clean up the unneeded methods from the learning instance - is longest path and highest fitnee needed hre or move it to generation data files
# DONE 6. Look at the agenet generator in relation to run generation - both use a loop that tracks the same thing - is the loop in the generator needed ?
# ISH 7. Can the creation of a new agent generatior be refactored down to not use the additional function call ? - is the partial needed ?


# 8. add the logging needed to show the data from a full run
# - Can the deco approach work without the need for the return in the fun ?
# Having to rebuild the whole logging file structure and process
# Look into how wrappers work better <---

# 9. Look at pygraph to also show the data

# Have a thin about re structuring of the system - treat each brain instance like a node, save its parents i.e the previous node - generating a tree format in the DB ?
# ID systm:

# generate an id and then add -b or -g for brain and generation ?
# Idea create a dict thats passed with the ID's to the Learnig instance, it can then assign from there

# Work out the structure of the generation_model and how each generation will be saved


# Add the passing of var data to the views - then add this to the testing

# Work out the ID system - final brain instance needs to be linked to each of the saved generations
# Or create an over arching model for each the inc the final brain and generation based data ?


# Add the var path to the URLS for the views - i.e the brain instance to be saved ect

# add generation_number to the brain instance model

# Work out how each Brain instance is going to be saved to the DB -
# New model for each instance ??

# Save each generational run i.e all the parents from a generation to a db
# Can serialize the who list of parents to make it easy with some extra details ect

# make view functions to:
# Get by generation number
# get highest fitness per generation number
# get longest path per generation

# model_data_formatting is messy and needs to be refactored down
# Clean up the config formats - need to match up the API to back end cofig files better

# Handling of the current_generation var for each instance
# This is now stored in the config fo each instance

# Write tests for the new setting of the brain_config/ann_config
# Also fix the naming of this var as it is confusing

# IDEAS

# Serialize/ picklejson the whole brain instance - just keep out the vars that want to be searchable
