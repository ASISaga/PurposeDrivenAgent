# CoderAgent is a class that defines a method execute_code() that uses the LocalCommandLineCodeExecutor to execute Python code.
# The code is executed in a local environment, and the output is displayed in the console.
# The code uses the PythonCodeExecutionTool to execute the code and the MagenticOne agent to interact with the user.
# The agent runs a stream of messages to complete a coding task, such as writing a Python script to fetch data from an API.
# The result of the task is displayed in the console. The CoderAgent class is used to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The purpose of this agent is to demonstrate the ability to execute code and interact with the user to complete a coding task autonomously. The agent uses the LocalCommandLineCodeExecutor to execute Python code and the PythonCodeExecutionTool to execute the code and display the output in the console. The agent uses the MagenticOne agent to interact with the user and complete the coding task. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent. The agent runs a stream of messages to complete the task and displays the result in the console. The CoderAgent class is used to demonstrate the
# ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent.
# The agent runs a stream of messages to complete the task and displays the result in the console.
# The CoderAgent class is used to demonstrate the ability to autonomously complete a coding task by executing Python code and interacting with the user using the MagenticOne agent.

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.teams.magentic_one import MagenticOne

class CoderAgent:
    def __init__(self, client, work_dir="coding"):
        self.client = client
        self.work_dir = work_dir

    async def execute_code(self):
        executor = LocalCommandLineCodeExecutor(work_dir=self.work_dir)
        tool = PythonCodeExecutionTool(executor)
        agent = AssistantAgent(
            "assistant", client=self.client, tools=[tool], reflect_on_tool_use=True
        )
        await Console(
            agent.run_stream(
                task="Create a plot of MSFT stock prices in 2024 and save it to a file. Use yfinance and matplotlib."
            )
        )

        m1 = MagenticOne(
            client=self.client
        )
        m1 = MagenticOne(client=self.client)
        # to enable human-in-the-loop mode, set hil_mode=True
        # m1 = MagenticOne(client=self.client, hil_mode=True)
        # To enable human-in-the-loop (HIL) mode, set hil_mode=True.
        result = await Console(
            m1.run_stream(task=task)
        )
        # which can be useful for tasks that require human judgment or decision-making.

        task = "Write a Python script to fetch data from an API."
        result = await Console(m1.run_stream(task=task))
        print(result)
