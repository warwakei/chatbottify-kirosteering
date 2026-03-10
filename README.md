 # Chatbottify

Steering rules for [Kiro IDE](https://kiro.dev) that make Claude AI more ChatGPT-like. Modern, fast, and straight to the point.

> **Huge respect to the Kiro team** — they're giving away Claude Haiku 4.5 with 400+ free requests, unlimited signups. That's insane. Go grab it at [kiro.dev](https://kiro.dev)

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

## Installation

### Option 1: Installer (Windows)
1. Download `ChatbottifyInstaller.exe` from [Releases](https://github.com/warwakei/chatbottify-kirosteering/releases)
2. Run the installer
3. Follow the prompts (it'll auto-detect your Kiro path)
4. Choose which extensions to install
5. Reload Kiro IDE

### Option 2: Manual
1. Clone or download this repo
2. Copy `.md` files from root to `C:\Users\[YourUsername]\.kiro\steering\`
3. Create the folder if it doesn't exist
4. Reload Kiro IDE

### Option 3: Per-Project
1. Copy `.md` files to `.kiro/steering/` in your project folder
2. Reload Kiro IDE

## Files

- `chatbottify.md` — main rule
- `chatbottify0-ext1.md` — code quality extension
- `chatbottify0-ext2.md` — deps/tests/docs extension

## Author

[warwakei](https://github.com/warwakei)

## License

MIT
