# Orange Erotic Bible

If [gpt-2](https://openai.com/blog/better-language-models/) read [literotica](http://literotica.com/), what would be its take on the Holy scriptures? 

[Entry](https://github.com/NaNoGenMo/2019/issues/18) to [NaNoGenMo](https://nanogenmo.github.io/) 2019.

## Samples

Read version 1.0 [here](https://write.as/409j3pqk81dazkla.md) or find it [here](the_orange_erotic_bible_v1.txt).

## Getting Started

### Prerequisites

- Python 3
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/)
- An erotica fine-tuned gpt-2 model. I am working on making mine available to download.
- A sense of humour, this is all in good Holy Spirits.

### Installing

```
cd orange-erotic-bible
pipenv install
```

### Generating

```
pipenv run python oeb/main.py --output_path={OUTPUT_PATH} --checkpoint_dir={CHECKPOINT_DIR}
```

- `OUTPUT_PATH`: txt file where to write the orange erotic bible
- `CHECKPOINT_DIR`: dir with fine-tuned gpt-2 checkpoint

## Running the tests

```
pipenv run pytest

```

## Built With

* [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple) - Wrapper for gpt-2 generation
* [nshepperd's gpt-2 fork](https://github.com/nshepperd/gpt-2/tree/finetuning) - Used for fine-tuning on erotic dataset
* [literotica](http://literotica.com/) - Erotic dataset
* [The Bible, King James Version](http://www.gutenberg.org/ebooks/30) - gpt-2 prompts

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
