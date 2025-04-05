# crypto_tracker_binance_sync.py
from mcp.server.fastmcp import FastMCP, Context, Image
import ccxt  # Use synchronous CCXT
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import json

# Initialize the MCP server
mcp = FastMCP("CryptoPortfolioMCP", dependencies=["ccxt", "matplotlib"])

# Binance API setup
binance = ccxt.binance({
    'enableRateLimit': True,
    # Uncomment and add your keys for authenticated features
    # 'apiKey': 'YOUR_API_KEY',
    # 'secret': 'YOUR_SECRET',
})
binance.httpsProxy = 'http://127.0.0.1:8118'

# Database setup
def init_db():
    conn = sqlite3.connect("portfolio.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY,
            coin_symbol TEXT,
            amount REAL,
            purchase_date TEXT
        )
    """)
    return conn

# Crypto price fetcher using Binance via CCXT (synchronous)
def get_crypto_price(symbol: str) -> float:
    ticker = binance.fetch_ticker(symbol.upper())
    return ticker['last']

# Tools with enhanced documentation
@mcp.tool()
def get_portfolio_summary() -> str:
    """
    Get current portfolio summary with total value using Binance prices.
    
    Returns:
        A string containing a formatted summary of all holdings with current
        prices and total portfolio value in USDT.
    
    Example:
        "Portfolio Summary (Binance Prices):\nBTC/USDT: 0.1 @ $60000.00 = $6000.00\nETH/USDT: 2.0 @ $2000.00 = $4000.00\nTotal Value: $10000.00"
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT coin_symbol, amount FROM holdings")
    holdings = cursor.fetchall()
    
    total_value = 0
    summary = ["Portfolio Summary (Binance Prices):"]
    for coin_symbol, amount in holdings:
        price = get_crypto_price(coin_symbol)
        value = price * amount
        total_value += value
        summary.append(f"{coin_symbol}: {amount} @ ${price:.2f} = ${value:.2f}")
    
    summary.append(f"Total Value: ${total_value:.2f}")
    conn.close()
    return "\n".join(summary)

@mcp.tool()
def add_holding(coin_symbol: str, amount: float) -> str:
    """
    Add a cryptocurrency holding to the portfolio.
    
    Parameters:
        coin_symbol (str): The trading pair symbol (e.g., "BTC/USDT" or "btc").
            If no "/USDT" is provided, it will be appended automatically.
            Case-insensitive.
        amount (float): The quantity of the cryptocurrency to add.
            Must be a positive number.
    
    Returns:
        A confirmation message indicating the holding was added.
    
    Example:
        add_holding("BTC", 0.1) -> "Added 0.1 BTC/USDT to portfolio"
    """
    if '/' not in coin_symbol:
        coin_symbol = f"{coin_symbol.upper()}/USDT"
    
    conn = init_db()
    conn.execute(
        "INSERT INTO holdings (coin_symbol, amount, purchase_date) VALUES (?, ?, ?)",
        (coin_symbol, amount, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return f"Added {amount} {coin_symbol} to portfolio"

@mcp.tool()
def get_price(coin_symbol: str) -> str:
    """
    Get current price for a cryptocurrency from Binance.
    
    Parameters:
        coin_symbol (str): The trading pair symbol (e.g., "ETH/USDT" or "eth").
            If no "/USDT" is provided, it will be appended automatically.
            Case-insensitive.
    
    Returns:
        A string with the current price in USDT.
    
    Example:
        get_price("ETH") -> "Current price of ETH/USDT on Binance: $2000.50"
    """
    if '/' not in coin_symbol:
        coin_symbol = f"{coin_symbol.upper()}/USDT"
    price = get_crypto_price(coin_symbol)
    return f"Current price of {coin_symbol} on Binance: ${price:.2f}"

@mcp.tool()
def portfolio_value_history(ctx: Context) -> Image:
    """
    Generate a chart of portfolio value over time using Binance prices.
    
    Parameters:
        ctx (Context): MCP context object for progress reporting.
            Automatically provided by the MCP framework.
    
    Returns:
        An Image object containing a PNG chart of portfolio value history.
    
    Notes:
        - Uses current prices for historical points (simplified implementation)
        - Chart shows value progression as holdings were added
    """
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT coin_symbol, amount, purchase_date FROM holdings ORDER BY purchase_date")
    holdings = cursor.fetchall()
    
    dates = []
    values = []
    current_holdings = {}
    
    for coin_symbol, amount, date in holdings:
        current_holdings[coin_symbol] = current_holdings.get(coin_symbol, 0) + amount
        date = datetime.fromisoformat(date)
        dates.append(date)
        
        total_value = 0
        for symbol, amt in current_holdings.items():
            price = get_crypto_price(symbol)
            total_value += price * amt
        values.append(total_value)
        ctx.info(f"Calculated value at {date}: ${total_value:.2f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values)
    plt.title("Portfolio Value Over Time (Binance Prices)")
    plt.xlabel("Date")
    plt.ylabel("Value (USDT)")
    plt.grid(True)
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    
    conn.close()
    return Image(data=buf.getvalue(), format="png")

# Prompts
@mcp.prompt()
def analyze_portfolio() -> str:
    """
    Analyze the current portfolio and suggest improvements.
    
    Instructions:
        Use the get_portfolio_summary tool to retrieve current holdings.
        Prices are sourced from Binance.
        Consider:
        - Diversification
        - Current market trends on Binance
        - Risk assessment
        Provide specific recommendations with reasoning.
    """
    return """
    Please analyze my cryptocurrency portfolio and suggest improvements.
    To get current holdings, use the get_portfolio_summary tool.
    Prices are sourced from Binance.
    Consider:
    - Diversification
    - Current market trends on Binance
    - Risk assessment
    Provide specific recommendations with reasoning.
    """

if __name__ == "__main__":
    # Initialize database
    init_db()
    # Run the server
    mcp.run()

    