"""Agent generation Factory"""


class AgentFactory:
    """Factory for agent selection"""

    agents = {}

    @classmethod
    def make_agent(cls, agent_type, brain, environment):
        """Generate the agent based on given type"""
        try:
            retreval = cls.agents[agent_type]
        except KeyError as err:
            raise NotImplementedError(f"{agent_type} is not implemented") from err

        return retreval(agent_brain=brain, environment=environment)

    @classmethod
    def register_agent(cls, agent_type):
        """Decorator to register the agent type"""

        def deco(deco_cls):
            cls.agents[agent_type] = deco_cls
            return deco_cls

        return deco


@AgentFactory.register_agent("Static_State")
class StaticStateMazeAgent:
    """Static state maze agent"""

    def __init__(self, environment: object, agent_brain: object):
        self.fitness: float = 0.0
        self.termination: bool = False
        self.brain: object = agent_brain
        self.environment: object = environment
        self.fitness_by_step: list[tuple] = []
        self.path: list[int, int] = [self.environment.current_coords]

    def run_agent(self) -> object:
        """Run the agent throught the environment"""

        while self.termination is False:
            observation_data = self.environment.get_environment_observation()
            action = self.brain.determin_action(observation_data)

            new_coords, termination_status, reward = self.environment.step(action)

            self.fitness += reward
            self.path.append(new_coords)
            self.termination = termination_status
            self.fitness_by_step.append(self.fitness)

        self.brain.fitness = self.fitness
        self.brain.traversed_path = self.path
        self.brain.fitness_by_step = self.fitness_by_step

        return self.brain
