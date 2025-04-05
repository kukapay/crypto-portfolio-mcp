# Crypto Portfolio MCP

An MCP server for tracking and managing cryptocurrency portfolio allocations, enabling AI agents to query and optimize portfolio strategies in real time.

![GitHub License](https://img.shields.io/github/license/kukapay/crypto-portfolio-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)


## Features

- **Portfolio Management**: Add and track cryptocurrency holdings with real-time Binance prices.
- **Price Retrieval**: Fetch current prices for any Binance trading pair (e.g., BTC/USDT).
- **Value History**: Generate visual charts of portfolio value over time.
- **Analysis Prompt**: Pre-built prompt for portfolio analysis with diversification and risk suggestions.
- **SQLite Storage**: Persistent storage of holdings in a local database.

## Installation

### Prerequisites
- Python 3.10+
- Git (optional, for cloning the repo)
- A compatible MCP client (e.g., [Claude Desktop](https://www.anthropic.com/claude))


### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/crypto-portfolio-mcp.git
   cd crypto-portfolio-mcp
   ```

2. **Install requirements**:
   ```bash
   pip install mcp[cli] ccxt matplotlib
   ```

3. **Install for Claude Desktop**:
   ```bash
   mcp install main.py --name "CryptoPortfolioMCP"
   ```
  
    Or update the configuration file manually:
  
    ```
    {
      "mcpServers": {
        "crypto-portfolio-mcp": {
          "command": "python",
          "args": [ "path/to/crypto-portfolio-mcp/main.py" ]
        }
      }
    }
    ```      

## Usage

Once installed, interact with the server through an MCP client like Claude Desktop. Below are example commands:

### Add a Holding
- **Prompt**: "Add 0.1 BTC to my portfolio"
- **Result**: Adds 0.1 BTC/USDT to your portfolio and confirms with "Added 0.1 BTC/USDT to portfolio".

### Get Current Price
- **Prompt**: "What's the current price of ETH on Binance?"
- **Result**: Returns "Current price of ETH/USDT on Binance: $2000.50" (example price).

### Portfolio Summary
- **Prompt**: "What's my current portfolio summary?"
- **Result**: Displays a formatted summary, e.g.:
  ```
  Portfolio Summary:
  BTC/USDT: 0.1 @ $60000.00 = $6000.00
  ETH/USDT: 2.0 @ $2000.00 = $4000.00
  Total Value: $10000.00
  ```

### Portfolio Value History
- **Prompt**: "Show me my portfolio value history"
- **Result**: Generates and displays a PNG chart of your portfolio value over time.

### Analyze Portfolio
- **Prompt**: "Analyze my crypto portfolio"
- **Result**: Provides an analysis with suggestions based on current holdings and Binance market trends.

## Tools

The server exposes the following tools:

- **`get_portfolio_summary`**: Retrieves a text summary of your current portfolio.
- **`add_holding(coin_symbol: str, amount: float)`**: Adds a cryptocurrency holding (e.g., "BTC", 0.1).
- **`get_price(coin_symbol: str)`**: Fetches the current price of a trading pair from Binance.
- **`portfolio_value_history()`**: Generates a PNG chart of portfolio value history.

See the source code docstrings for detailed parameter descriptions.

## Database

Holdings are stored in a SQLite database (`portfolio.db`) with the following schema:
```sql
CREATE TABLE holdings (
    id INTEGER PRIMARY KEY,
    coin_symbol TEXT,       -- e.g., "BTC/USDT"
    amount REAL,           -- Quantity of the asset
    purchase_date TEXT     -- ISO format timestamp
)
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
