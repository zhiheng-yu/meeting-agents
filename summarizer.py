import os
from agno.agent import Agent
from agno.models.openai import OpenAILike


local_dir = os.path.dirname(__file__)
minutes_format_path = os.path.join(local_dir, "config", "minutes_format.md")
with open(minutes_format_path, "r", encoding='utf-8') as f:
    minutes_format = f.read()

system_prompt_path = os.path.join(local_dir, "config", "summary_prompt.md")
with open(system_prompt_path, "r", encoding='utf-8') as f:
    system_prompt = f.read()

system_prompt = system_prompt.replace("{{minutes_format}}", minutes_format)

qwen_model = OpenAILike(
    id=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

summary_agent = Agent(
    model=qwen_model,
    name="summary_agent",
    description="A summary agent that summarizes the meeting",
    instructions=[system_prompt]
)

if __name__ == '__main__':
    file_path = input("选择需要总结的会议转录文件: ")
    file_name, file_format = os.path.splitext(file_path)

    with open(file_path, "r", encoding='utf-8') as f:
        conversation = f.read()

    summary_agent.print_response(conversation, stream=True)
