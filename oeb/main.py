import logging
import fire
import generators
import prompts

logging.basicConfig(level=logging.INFO)

BIBLE_PATH = "resources/kjbible_prompts.txt"
EXPLICIT_VOCAB_PATH = "resources/explicit_vocab.txt"

def write(output_path,
          checkpoint_dir,
          run_name="oeb1",
          bible_path=BIBLE_PATH,
          explicit_vocab_path=EXPLICIT_VOCAB_PATH,
          window_size=15,
          step_size=8,
          maxsentences=8,
          minsentences=6,
          gen_length=1000):

    # Decorated generators
    generator = generators.GPT2Generator(checkpoint_dir=checkpoint_dir, run_name=run_name)
    generator = generators.SentenceTruncation(generator, maxsentences=maxsentences, minsentences=minsentences)
    generator = generators.ExplicitFilter(generator, explicit_vocab_path)
    generator = generators.TokenFilter(generator)

    oeb_prompts = prompts.bible_prompts(bible_path=bible_path,
                                        window_size=window_size,
                                        step_size=step_size)
    oeb_lines = generate_oeb_lines(generator, oeb_prompts, gen_length)

    for line in oeb_lines:
        with open(output_path, 'a') as o:
            o.write(line + '\n')


def generate_oeb_lines(generator, oeb_prompts, gen_length):
    for prompt, content in oeb_prompts:
        generation = generator.generate(prefix=prompt, length=gen_length)
        yield generation


if __name__ == '__main__':
    fire.Fire(write)
