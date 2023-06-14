import json, re
from pathlib import Path

with open(Path(__file__).parent /"crawler-user-agents.json") as file:
    crawler_user_agents = json.load(file)

patterns = (crawler["pattern"] for crawler in crawler_user_agents)
CRAWLER_USER_AGENT_REGEX = re.compile("|".join(patterns))

def is_crawler(user_agent):
    return CRAWLER_USER_AGENT_REGEX.search(user_agent) is not None
