from llm import Assistant
from tts import text_to_speech 
from process_text import split_text

# split text into paragraphs 
paragraphs = split_text(
    filename='file.txt',
    paragraph_len=200
)

print(len(paragraphs))

# estimate the costs 
voice_costs_per_1k_chars = 0.015
text_costs_per_1k_toks = 0.01

chars = len("".join(paragraphs))
toks = len("".join(paragraphs).split(" "))

print(chars, toks) 

voice_cost = round(chars/1000 * voice_costs_per_1k_chars, 2)
text_cost = round(toks/1000 * text_costs_per_1k_toks * 2, 2)

print(f'estimated costs: \nvoice: ${voice_cost}\ntext: ${text_cost} \ntotal: ${round(voice_cost + text_cost, 2)}\n')

# confirm and proceed to summarize + generate audio 
confirm = input('confirm? y/n ')

if confirm == 'y':
    idx = 0 

    for paragraph in paragraphs[100:105]:
        print(paragraph)
        print('*'*30)

    for paragraph in paragraphs[100:105]:
        # create a new assistant each time to save token costs
        summarizer = Assistant(
            system_prompt="Summarize the passage in two sentences.",
            model="gpt-3.5-turbo"
        )
        print(paragraph)
        
        summary = summarizer.get_completion(f'PASSAGE: {paragraph}')
        text_to_speech(summary, max_len=400, idx=idx)
