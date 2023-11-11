class agent:
    def __init__(self) -> None:
        self.loc = 0

    def run(self):
        self.loc = 1


def test_gen():
    for x in range(10):
        agent.run(agent)
        yield agent


gen = test_gen()

post_run = [agent for agent in gen]

print(post_run[0].loc)
