# def get_highest_fitness_brain(self, parents: list[BrainInstance]) -> object:
#         """
#         Get the highest fitness brain from the list of parents
#         var: parents - the given range of brains
#         rtn: highest_fitness_brain - the brain instance with the highest fitness
#         """
#         if not parents:
#             return None
#         highest_fitness_brain = max(parents, key=attrgetter("fitness"))

#         return highest_fitness_brain

#     def get_longest_path_brain(self, parents: list[BrainInstance]) -> object:
#         """
#         Get the longest path brain instances
#         var: parents - the given range of brains
#         rtn: longest_path_brain - the brain instance with the longest path
#         """

#         if not parents:
#             return None
#         longest_path_brain = parents[0]
#         for brain in parents:
#             if len(brain.traversed_path) > len(longest_path_brain.traversed_path):
#                 longest_path_brain = brain

#         return longest_path_brain


# def test_get_longest_path(parent_data, learning_instance) -> None:
#     """Get the brain instance longest path from a set of given brains"""
#     longest_path_brain_instance: BrainInstance = (
#         learning_instance.get_longest_path_brain(parents=parent_data)
#     )
#     assert len(longest_path_brain_instance.traversed_path) == number_of_test_brains - 1


# def test_get_highest_fitness(parent_data, learning_instance) -> None:
#     """Get the highest fitness brain instance from a set of given brains"""
#     highest_fitness_brain_instance: BrainInstance = (
#         learning_instance.get_highest_fitness_brain(parents=parent_data)
#     )
#     assert highest_fitness_brain_instance.fitness == number_of_test_brains - 1
