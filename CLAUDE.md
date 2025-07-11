# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese Xiehouyu (歇后语) interactive game project that provides both exploration utilities and a web-based two-player competition game. The project includes a dataset of 14,032 traditional Chinese two-part allegorical sayings and a modern web interface built with NiceGUI.

## Development Environment

This project uses uv for Python dependency management and execution:

- **Run main game**: `uv run xiehouyu_game.py`
- **Run explorer**: `uv run xiehouyu_explorer.py`
- **Add dependencies**: `uv add <package_name>`
- **Python version**: Requires Python ≥3.13 (specified in pyproject.toml)

## Core Architecture

### Data Structure
- **Primary dataset**: `xiehouyu.json` - 14,032 entries with `riddle` and `answer` fields
- **Data format**: JSON array of objects with Chinese text encoded in UTF-8
- **Answer format**: Some answers contain multiple options separated by Chinese semicolons (；)

### Main Components

**Game Components**:
- **`game_logic.py`**: Core game logic with dual-question system, simplified scoring, no timers
- **`game_ui.py`**: NiceGUI-based UI with two-column layout, integrated player panels
- **`xiehouyu_game.py`**: Main game application with child-friendly Bento Grid design

**Explorer Components**:
- **`xiehouyu_explorer.py`**: Utility class for dataset analysis and exploration
- **`demo_usage.py`**: Feature demonstration script

### Game Features

**Game Mechanics**:
- Two-player competition with separate riddles per player each round
- No time pressure - players can think at their own pace
- Visual masking of answer options using CSS boxes instead of question marks
- Simplified scoring system with difficulty-based bonuses
- Streak tracking for consecutive correct answers

**UI Design**:
- Modern Bento Grid layout with child-friendly colors
- Two-column layout with integrated player panels
- Prominent start button at the top (no scrolling needed)
- Responsive design for different screen sizes
- CSS animations for feedback and visual effects

## Common Commands

```bash
# Run the main game (web interface)
uv run xiehouyu_game.py

# Run the explorer with interactive mode
uv run xiehouyu_explorer.py

# Run feature demonstration
uv run demo_usage.py

# Test game logic
uv run test_game.py
```

## Game URLs

When running the game:
- **Main game**: `http://localhost:8080/`
- **Statistics**: `http://localhost:8080/statistics`
- **Help**: `http://localhost:8080/help`

## Data Characteristics

- **Dataset size**: 14,032 total entries
- **Unique riddles**: 14,031 (minimal duplication)
- **Unique answers**: 9,117 (many riddles share answers)
- **Multi-answer riddles**: 2,458 entries with multiple answer options
- **Text encoding**: UTF-8 Chinese characters
- **Average lengths**: ~6 characters per riddle, ~5.5 per answer

## Game Design Philosophy

The game is designed to be:
- **Educational**: Helps players learn traditional Chinese culture
- **Relaxed**: No time pressure, encouraging thoughtful consideration
- **Accessible**: Child-friendly interface with clear visual feedback
- **Engaging**: Modern UI with animations and interactive elements

## Technical Implementation

**Frontend**: NiceGUI with custom CSS styling
**Backend**: Python with asyncio for game flow management
**Architecture**: Component-based design with separation of concerns
**Styling**: Modern gradients, shadows, and animations following Bento Grid principles