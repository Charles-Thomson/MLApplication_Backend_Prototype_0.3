# TODO NEXT


# TODAY
# Work out the structure of the generation_model and how each generation will be saved

# Set up the saving of the generation_models inc formatting ect

# Add the passing of var data to the views - then add this to the testing

# Work out the ID system - final brain instance needs to be linked to each of the saved generations
# Or create an over arching model for each the inc the final brain and generation based data ?

# Set up test for the generation_models - adding and getting from db

# Clean up the adding/getting and formatting of database models - it's messey currently


# Build the generation data config on the running of instance func

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
