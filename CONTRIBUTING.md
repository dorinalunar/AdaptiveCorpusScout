# Contributing to AdaptiveCorpusScout

First off, thank you for considering contributing to AdaptiveCorpusScout!

## Development Workflow

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/amazing-feature`).
3. Make your changes and write tests for them.
4. Ensure all tests pass locally (`pytest test_corpus_scout.py -v`).
5. Commit your changes (`git commit -m 'Add amazing feature'`).
6. Push to the branch (`git push origin feature/amazing-feature`).
7. Open a Pull Request.

## Testing Guidelines
Any new features or modifications to the GenLayer Intelligent Contract logic must include corresponding `pytest` cases in `test_corpus_scout.py`. Ensure that Laplace allocation logic and AI verdict extraction remain deterministic.
