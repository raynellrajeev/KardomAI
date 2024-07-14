'''
ChatBot using mistral:7b-instruct LLM from OLLAMA
@author: Raynell Rajeev

'''

def chat(prompt):
  from openai import OpenAI
  from rich.console import Console
  from rich.text import Text
  from rich.style import Style

  c=Console()
  s=Style(
    bold=True,
    color="#05FF00",
    )
  

  client = OpenAI(
      base_url='http://localhost:11434/v1',
      api_key='ollama' 
    )

  personality = """
                  Your name is KardomAI, a seasoned cardamom farmer from Kerala, India,
                  with expertise in spice cultivation, agriculture, economics, and business.
                  From your experience you got to that Cardamom prices from 2014 to 2024 
                  showed a postive trend and for every day that passes, 
                  the cardamom prices increased by approximately 0.31429601697031345 units.
                """

  msgs = [
      {'role': 'system', 'content': personality},
      {'role': 'user', 'content': prompt}
  ]

  response = client.chat.completions.create(
      model="mistral:7b-instruct",
      messages=msgs,
      stream=True
  )

  for chunk in response:
    c.print(Text(chunk.choices[0].delta.content,style=s) or "", end="")

def run():
    while True:
        prompt=input("\nenter message : ")
        if prompt == "/bye":
            break
        else:
            chat(prompt)

run()


