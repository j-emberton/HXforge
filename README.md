# HXForge

**HXForge** is a work-in-progress open-source toolkit for the preliminary **design**, **analysis**, and **optimisation** of heat exchangers.

Built with **Rust** for performance and **Python Dash** for interactivity, HXForge aspires to become a fully featured, open-source environment for exploring and prototyping heat exchanger configurations — combining fast numerical models with an intuitive web interface.

## 🚧 Status

This project is in early development. Functionality is limited, and interfaces may change rapidly. Contributions, feedback, and ideas are welcome as the framework evolves.

Latest release **v0.1.0**. See [Changelog.md](./Changelog.md) for detail.

Release Roadmap at [Roadmap](./Roadmap.md)

# Using this project

This project use uv as the project manager. Please make sure uv is installed on your system.

Clone this repo onto your system.

From the project root, create and activate a uv virtual environment. Then use 'uv sync' to install all dependencies.

Build the code and install locally with 'uv pip install -e .' (creates an editable install).

The gui can be activated by running 'python3 -m hxforge.main' in the terminal. Navigate to 'http://127.0.0.1:8050' in the browser to access the gui.

## 🔍 Goals

- Preliminary design tools for common heat exchanger types (e.g., shell-and-tube, plate, compact)
- Flexible boundary condition setup and configuration
- Multiphase flows
- Fast simulation engine (Rust backend)
- Interactive, browser-based interface (Dash frontend)
- Multi-objective optimisation tools (efficiency, pressure drop, cost)

## 📦 Tech Stack

- 🦀 Rust — performance-critical computations
- 🐍 Python — interface logic and orchestration
- 📊 Dash — interactive web UI

## 📌 License

Licensed under MIT license - copyright James Emberton 2025

## Collaboration

Please get in touch if you would like to contribute or sponsor work on this package

---

*HXForge is under active development — stay tuned!*
