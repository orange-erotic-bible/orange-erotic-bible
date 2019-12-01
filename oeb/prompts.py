import logging
import os

def bible_prompts(bible_path, window_size=10, step_size=10):
    """bible_prompter

    Prompt generator which returns consecutive chunks of the bible.
    :param window_size: number of lines per chunk
    :param step_size: number of lines to shift by at each iteration 
    """
    with open(bible_path, 'r') as f:
        lines = f.readlines()
        logging.info(f'loaded {len(lines)} bible lines')
    for  x in range(0, len(lines), step_size):
        prompt = ''.join(lines[x:x+window_size]), ''.join(lines[x:x+step_size])
        logging.info("New Bible Prompt")
        logging.debug(prompt)
        yield prompt


def feedback_prompts(output_path, window_size=10, step_size=1):
    """feedback_prompter

    Prompt generator which returns consecutive sliding windows of the orange
    erotic bible, and appends to it another bible line.

    :param window_size: Size of sliding window
    :param step_size: number of lines to shift by at each iteration 
    """
    with open(BIBLE_PATH, 'r') as f:
        bible_lines = f.readlines()
        logging.info(f'loaded {len(bible_lines)} bible lines')
    chunks = list(chunkify(bible_lines, step_size))
    i = 0
    while i < len(chunks):
        last_oeb_lines = os.popen(f'tail -n {window_size - step_size} {output_path}').read()
        prefix = chunks[i]
        yield last_oeb_lines + prefix, prefix
        i += 1
    raise StopIteration


def chunkify(lines, chunk_size):
    return (''.join(lines[x: x+chunk_size]) for x in range(0, len(lines), chunk_size))
