from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class FlanAlpacaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""{context}
=====
"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    input = "" if pingpong.input is None or pingpong.input == "" else f"{pingpong.input[:truncate_size]}\n-----"
    return f"""
{pingpong.ping[:truncate_size]}
{input}
-----
{"" if pingpong.pong is None or pingpong.pong == "" else pingpong.pong[:truncate_size]}"""

class FlanAlpacaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=FlanAlpacaPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

      if from_idx+idx != to_idx-1:
        results += """
-----
"""

    return results

