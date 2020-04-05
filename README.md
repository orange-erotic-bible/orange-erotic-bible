# :pray: Orange Erotic Bible :two_hearts:

If [gpt-2](https://openai.com/blog/better-language-models/) read [literotica](http://literotica.com/), what would be its take on the Holy scriptures? 

[Entry](https://github.com/NaNoGenMo/2019/issues/18) to [NaNoGenMo](https://nanogenmo.github.io/) 2019.

## Samples

Read the Orange Erotic Bible version 1.0 on [write.as](https://write.as/409j3pqk81dazkla.md), or as a [.txt file](the_orange_erotic_bible_v1.txt).

## Getting Started

### Prerequisites

- Python 3.7
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/)
- A sense of humour, this is all in good Holy Spirits.

### Installing

#### Download model

To generate a new orange erotic bible, you need an erotica fine-tuned gpt-2 model.  
Download mine from google drive [here](https://drive.google.com/open?id=1hcPVn7-F_pN6Pir8oPEI7-SVqcfJ7043). Use that `checkpoint_dir` path as `--checkpoint_dir` argument to the generation script below.  
Alternatively, fine tune gpt-2 with some steamy literature and use your own erotic language model.

#### Install Dependencies

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
