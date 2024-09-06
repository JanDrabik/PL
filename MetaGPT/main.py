import re

import fire

from metagpt.actions import Action
from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from metagpt.team import Team
from metagpt.environment import Environment
from metagpt.roles import ProductManager


def parse_code(rsp):
    pattern = r"```python(.*)```"
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    return code_text


class WriteCode(Action):
    PROMPT_TEMPLATE: str = """
    You are a senior python developer that can write any code requested.
    Write a python function that can {instruction} and provide two runnable test cases if possible.
    Your output message should be only the code you produced.
    """

    name: str = "WriteCode"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        code_text = parse_code(rsp)
        return code_text


class Coder(Role):
    name: str = "James"
    profile: str = "Senior Coder"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteCode])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg


class WriteReview(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Review the test cases and provide one critical comments:
    """

    name: str = "WriteReview"

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        code_text = parse_code(rsp)
        return code_text


class WriteTest(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    You are an expert software tester.
    Write {k} unit tests using pytest for the given function, assuming you have imported it.
    Your output message should be only the code you produced.
    """

    name: str = "WriteTest"

    async def run(self, context: str, k: int = 3):
        prompt = self.PROMPT_TEMPLATE.format(context=context, k=k)
        rsp = await self._aask(prompt)
        code_text = parse_code(rsp)
        return code_text


class Tester(Role):
    name: str = "Jessie"
    profile: str = "Senior Tester"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteTest, WriteReview])
        self._watch([WriteCode])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        context = self.get_memories()
        code_text = await todo.run(context, k=5)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        return msg


async def main(
        idea: str = "Write a 2048 game in python using pygame. "
                    "User most importantly should be able to start the game, "
                    "see his current score, use arrows keys to control tiles "
                    "movement and see game over screen if he cant make any moves. "
                    "Each color tile changes based on the number on tiles.",
        investment: float = 2.0,
        n_round: int = 10,
):
    logger.info(idea)

    env = Environment(desc="Software house")
    team = Team(env=env, roles=[ProductManager(), Coder(), Tester()], investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round, idea=idea, send_to="ProductManager")


if __name__ == "__main__":
    fire.Fire(main)
