# Chatbottify

Steering rules for Kiro IDE that make Claude AI more ChatGPT-like. Modern, fast, and straight to the point.

## What's this?

Set of steering rules that change how Claude behaves in Kiro:
- ChatGPT-style communication
- Less fluff, more facts
- Quick and efficient answers
- Focus on code quality, tests, and docs

## Rules

**Chatbottify** — main rule, makes Claude talk like ChatGPT

**Extension 1** — code quality & efficiency (typing, clean code, bug fixes)

**Extension 2** — dependencies, tests & docs (version checks, test patterns, documentation)

## Setup

1. Copy `.md` files to `.kiro/steering/` in your project
2. Reload Kiro IDE
3. Done, rules apply automatically

## Files

- `chatbottify.md`
- `chatbottify0-ext1.md`
- `chatbottify0-ext2.md`

## Author

[warwakei](https://github.com/warwakei)

## License

MIT
