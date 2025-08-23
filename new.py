from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl, weather



agent = Agent(tools=[calculator, current_time, python_repl,weather])

message = """
What is the current time?
"""

agent(message)