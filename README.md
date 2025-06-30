# Decision Making Toolkit

A comprehensive toolkit for applying decision-making frameworks to evaluate strategic options and business decisions.

## Features

- **Multiple Frameworks**: Supports 5 key decision-making frameworks:
  - McKinsey 7S Framework
  - VPC (Value-Price-Cost) Model
  - Strategic Inflection Points
  - Game Theory Analysis
  - Risk-Reward Matrix

- **CLI Interface**: Interactive command-line tool for guided analysis
- **Web Interface**: User-friendly web application with visualizations
- **Data Persistence**: YAML-based storage system for decision tracking

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
# List available frameworks
python cli.py --list-frameworks

# Create a new decision
python cli.py --create "Should we launch Product X in the European market?"

# Apply a framework to a decision
python cli.py --decision should-we-launch-product-x-in --framework 7s

# Interactive mode for comprehensive analysis
python cli.py --decision should-we-launch-product-x-in --interactive

# View results
python cli.py --decision should-we-launch-product-x-in --view
```

### Web Interface

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## Framework Details

### McKinsey 7S Framework
Analyzes organizational alignment across 7 dimensions:
- Strategy, Structure, Systems, Shared Values, Style, Staff, Skills
- Provides overall alignment score and identifies weak areas
- Benchmark: >7.5 indicates readiness for strategic initiatives

### VPC Framework
Evaluates business model through Value-Price-Cost relationships:
- Calculates margins and value premiums
- Classifies strategy type (Cost Leadership, Differentiation, etc.)
- Provides competitive positioning insights

### Strategic Inflection Points
Identifies when fundamental business changes are needed:
- Assesses market signals and competitive threats
- Evaluates internal readiness for transformation
- Recommends Transform, Prepare, or Defend strategies

### Game Theory
Analyzes competitive interactions and strategic moves:
- Models player actions and payoff matrices
- Identifies Nash equilibria and dominant strategies
- Provides strategic move recommendations

### Risk-Reward Matrix
Evaluates strategic options across risk and reward dimensions:
- Calculates risk-adjusted returns and efficiency ratios
- Categorizes options into priority quadrants
- Provides portfolio prioritization guidance

## Data Storage

Decision data is stored in YAML format in the `data/` directory. Each file contains:
- Decision text and metadata
- Framework inputs and results
- Timestamps and progress tracking

## Architecture

```
tools/
├── frameworks/          # Framework implementations
│   ├── framework_base.py
│   ├── seven_s_framework.py
│   └── ...
├── cli/                # CLI utilities
│   └── decision_manager.py
├── templates/          # Web templates
├── cli.py             # CLI interface
├── app.py             # Web application
└── data/              # Decision storage
```

## Contributing

Each framework extends the base `Framework` class and implements:
- `get_required_inputs()`: Define input schema
- `validate_inputs()`: Input validation
- `calculate()`: Core logic and scoring
- `get_visualization_data()`: Chart data

## License

Academic use only - Harvard Decision Making Course toolkit.