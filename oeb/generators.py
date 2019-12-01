import logging
import gpt_2_simple as gpt2
import re
import itertools


class GPT2Generator:
    """GPT2Generator

    Loads given GPT2 checkpoint, then generates text from prompt."""

    def __init__(self, checkpoint_dir, run_name):
        self.checkpoint_dir = checkpoint_dir
        self.run_name = run_name
        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess,
                run_name=self.run_name,
                checkpoint_dir=self.checkpoint_dir,
                model_name=None,
                model_dir='models')

    def generate(self, **kwargs):
        generations = gpt2.generate(self.sess,
                run_name=self.run_name,
                checkpoint_dir=self.checkpoint_dir,
                top_k=0,
                top_p=0.95,
                temperature=1.0,
                nsamples=1,
                batch_size=1,
                return_as_list=True,
                include_prefix=True,
                truncate=None,
                **kwargs)
        generations = [self.filter_prefix(gen, kwargs.get('prefix')) for gen in generations]
        logging.info("GPT2Generator success")
        logging.debug(generations[0])
        return generations[0]

    def filter_prefix(self, generation, prefix):
        return generation[len(prefix):]


class SentenceTruncation:

    def __init__(self, generator, maxsentences=100, minsentences=1):
        self.generator = generator
        self.MAX_RETRIES = 100
        self.maxsentences = maxsentences
        self.minsentences = minsentences

    def generate(self, **kwargs):
        generation = ""
        i = 0
        while i < self.MAX_RETRIES:
            i += 1
            logging.info(f"sentence truncation generator, attempt {i}")
            generation = self.generator.generate(**kwargs)
            sentences = self.split_sentences(generation)
            if len(sentences) >= self.minsentences:
                logging.info("SentenceTruncation success")
                offset = self.get_truncation_offset(sentences, self.maxsentences)
                return generation[:offset]
            else: 
                logging.info("SentenceTruncation failure: not enough sentences generated. retrying")
        raise Exception("Can't generate enough sentences after {self.MAX_RETRIES} retries")

    def split_sentences(self, content):
        sentences = re.split("[.?!]", content)
        # always discard last incomplete sentence
        return sentences[:-1]

    def get_truncation_offset(self, sentences, maxsentences):
        """get_truncation_offset

        This maintains original punctuation.

        :param sentences:
        :param maxsentences:
        """
        offset = 0 
        if len(sentences) < maxsentences:
            logging.warning("Not enough sentences to truncate, skipping truncation")
        for s in sentences[:maxsentences]:
            offset += len(s) + 1
        return offset


class ExplicitFilter:

    def __init__(self, generator, explicit_vocab_path):
        self.generator = generator
        self.explicit_vocab_path = explicit_vocab_path
        self.explicit_vocab = self.load_vocab(self.explicit_vocab_path)
        self.MAX_RETRIES = 100

    def load_vocab(self, input_path):
        with open(input_path, 'r') as f:
            lines = f.readlines()
            return [line.strip() for line in lines]

    def generate(self, **kwargs):
        generation = ""
        i = 0
        while not self.is_explicit(generation):
            i += 1
            logging.info(f"explicit filter generator, attempt {i}")
            if i == self.MAX_RETRIES:
                raise Exception(f"Can't generate explicit content after {self.MAX_RETRIES} retries")
            generation = self.generator.generate(**kwargs)
        return generation

    def is_explicit(self, content):
        explicit_mask = [gram in content.lower() for gram in self.explicit_vocab]
        answer = any(explicit_mask)
        if answer:
            logging.info("ExplicitFilter success")
            logging.debug(f'explicit terms: {list(itertools.compress(self.explicit_vocab, explicit_mask))}')
        else:
            logging.info("ExplicitFilter failure: no explicit terms found. retrying")
        return answer


class TokenFilter:

    def __init__(self, generator, token_list=['<|startoftext|>', '<|endoftext|>']):
        assert token_list
        self.token_list = token_list
        self.generator = generator
        self.MAX_RETRIES = 100

    def generate(self, **kwargs):
        generation = self.token_list[0]
        i = 0
        while self.contains_bad_tokens(generation):
            i += 1
            logging.info(f"token filter generator, attempt {i}")
            if i == self.MAX_RETRIES:
                raise Exception(f"Can't generate correct content after {self.MAX_RETRIES} retries")
            generation = self.generator.generate(**kwargs)
        return generation

    def contains_bad_tokens(self, content):
        mask = [token in content for token in self.token_list]
        answer = any(mask)
        if answer:
            logging.info("TokenFilter failure: found forbidden tokens")
            logging.debug(f'forbidden tokens: {list(itertools.compress(self.token_list, mask))}')
        else:
            logging.info("TokenFilter success")
        return answer


class TestGenerator:

    def generate(self, prompt=None):
        return 'miaow'
