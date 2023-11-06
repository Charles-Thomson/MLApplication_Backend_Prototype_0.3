# TODO Today:

# Next with GQL
# DONE 1. create a schema and resolver for getting a leraning instance
# DONE 2. Test getting a learning instance by the learning instance id
# DONE 3. create a resolver for the generations model
# DONE 4. test getting generations based on the learning instance FK
# DONE 5. create schema and resolver for brain_instances
# DONE 6. test getting brain instances from the generation instance FK

# Able to get each model by the ref to the "parent" models id
# Need a way of keeping track of the parent model id's

# Next:
# 1. passing in of the input_config data
# 2. Running of the system base don the passed in input_config
# 3. getting the return data from the run - will need the instance_id and and data re generations ?
# 4. getting the most alpah brain from a run


# WORKING ON
# The get by fk is getting using the learning instances ID - not the ref retunred


# 1. Look at the data plotting from version_0.2 ?
# Implement if simple

# 2. Start looking into the Azure database hosting


# Future
# 1. The id system is poor and needs to be resolved
# 2. Is the gernation ID the same as the DB ref from instance/generations
# 3. Look into GQL for API stuff
# 4. Logging generation and Decos can be refactored down - makred with TODO tags
# 5. Define the option to select the root for the logging files
