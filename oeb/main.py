from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import logging
import fire
import generators
import prompts
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

BIBLE_PATH = "resources/kjbible_prompts.txt"
EXPLICIT_VOCAB_PATH = "resources/explicit_vocab.txt"
RUN_NAME="oeb"

def write(output_path,
          checkpoint_dir,
          run_name=RUN_NAME,
          bible_path=BIBLE_PATH,
          explicit_vocab_path=EXPLICIT_VOCAB_PATH,
          window_size=15,
          step_size=8,
          maxsentences=8,
          minsentences=6,
          gen_length=1000,
          verbose=False):

    if verbose:
        logging.basicConfig(level=logging.INFO)
    # Decorated generators
    generator = generators.GPT2Generator(checkpoint_dir=checkpoint_dir, run_name=run_name)
    generator = generators.SentenceTruncation(generator, maxsentences=maxsentences, minsentences=minsentences)
    generator = generators.ExplicitFilter(generator, explicit_vocab_path)
    generator = generators.TokenFilter(generator)

    oeb_prompts = prompts.bible_prompts(bible_path=bible_path,
                                        window_size=window_size,
                                        step_size=step_size)
    oeb_lines = generate_oeb_lines(generator, oeb_prompts, gen_length)

    print('Starting orange erotic bible generation, this may take a while')
    for line in oeb_lines:
        print(line)
        with open(output_path, 'a') as o:
            o.write(line + '\n')


def generate_oeb_lines(generator, oeb_prompts, gen_length):
    for prompt, content in oeb_prompts:
        generation = generator.generate(prefix=prompt, length=gen_length)
        yield generation


if __name__ == '__main__':
    fire.Fire(write)
