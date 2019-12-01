from context import oeb
import pytest

def test_explicit_filter():
    test_generator = ConfigurableGenerator()
    explicit_filter_generator = oeb.generators.ExplicitFilter(test_generator, "resources/explicit_vocab.txt")

    generation = explicit_filter_generator.generate(content="Fuck yes it's explicit.\nIt's explicit as ballz")
    assert generation

    with pytest.raises(Exception):
        generation = explicit_filter_generator.generate(content="Not an explicit line.")

def test_token_filter():
    test_generator = ConfigurableGenerator()
    token_filter_generator = oeb.generators.TokenFilter(test_generator)

    generation = token_filter_generator.generate(content="this one is fine")
    assert generation

    with pytest.raises(Exception):
        generation = token_filter_generator.generate(content="this does contain a stop token. <|endoftext|> Annoying no?")

def test_sentence_truncation():
    test_generator = ConfigurableGenerator()
    token_filter_generator = oeb.generators.SentenceTruncation(test_generator)
    generation = token_filter_generator.generate(content="This is a fine sentence.")
    assert len(generation) == 24
    token_filter_generator = oeb.generators.SentenceTruncation(test_generator, maxsentences=2)
    generation = token_filter_generator.generate(content="This is also a fine sentence. In fact there are many cool sentence! Check this one out.  Have you seen it though? Oh wait a truck is coming towa")
    assert len(generation) == 67
    with pytest.raises(Exception):
        token_filter_generator = oeb.generators.SentenceTruncation(test_generator, minsentences=2)
        generation = token_filter_generator.generate(content="This is not long enough I'm afraid!", minsentences=2)

class ConfigurableGenerator:

    def generate(self, content):
        return content

