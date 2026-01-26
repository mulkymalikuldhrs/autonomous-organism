from enum import Enum

class AgentType(Enum):
    RESEARCH = "research"
    BUILDER = "builder"
    GROWTH = "growth"
    SUPPORT = "support"

class Agent:
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.is_alive = True

    def run(self):
        # Placeholder for agent's main loop
        pass

    def kill(self):
        self.is_alive = False

def spawn_agent(agent_type: AgentType):
    """
    Spawns a new agent.
    """
    agent = Agent(agent_type)
    # In a real implementation, this would run in a separate process or thread
    return agent
