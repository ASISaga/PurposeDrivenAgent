# Autonomously complete a coding task:
import asyncio

from config import model
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_agentchat.ui import Console


from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.agents.file_surfer import FileSurfer

client = OpenAIChatCompletionClient(model=model)


async def FileWebSurferAgent() -> None:
    # Define web surfer agent
    web_surfer_agent = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        model_client=OpenAIChatCompletionClient(model=model),
    )

    # Define file surfer agent
    file_surfer_agent = FileSurfer(
        name="FileSurfer",
        model_client=OpenAIChatCompletionClient(model=model),
    )

    # Define a team
    agent_team = RoundRobinGroupChat([web_surfer_agent, file_surfer_agent], max_turns=3)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="Navigate to the AutoGen readme on GitHub.")
    await Console(stream)
    # Close the browser controlled by the agent
    await web_surfer_agent.close()

