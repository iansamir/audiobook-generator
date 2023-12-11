
def split_text(filename, paragraph_len):
    
    with open(filename, 'r') as file:
        text = file.read()
        toks = text.split(' ')

    paragraphs = [] 
    idx = 0
    curr_paragraph = ''

    while idx < len(toks):
        if len(curr_paragraph.split()) >= paragraph_len:
            paragraphs.append(curr_paragraph)
            curr_paragraph = ''

        curr_paragraph += toks[idx] + ' '

        idx += 1

    if curr_paragraph:
        paragraphs.append(curr_paragraph)

    return paragraphs 

