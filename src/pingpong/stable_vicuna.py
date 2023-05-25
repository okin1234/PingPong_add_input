from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class StableVicunaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""{context}

"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    input = "" if pingpong.input is None or pingpong.input == "" else f"### Input: {pingpong.input[:truncate_size]}"
    ping = pingpong.ping[:truncate_size]
    pong = "" if pingpong.pong is None or pingpong.pong == "" else pingpong.pong[:truncate_size]
    return f"""
{input}
### Human: {ping}
### Assistant: {pong}
"""

class StableVicunaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=StableVicunaPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

    return results