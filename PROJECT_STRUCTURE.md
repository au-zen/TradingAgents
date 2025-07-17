# Project Structure

This document outlines the structure of the TradingAgents project, a multi-agent LLM-based framework for financial trading.

## Core Components

- **`cli/main.py`**: The entry point for the command-line interface (CLI). It uses the `typer` library to create a user-friendly interface for running the trading analysis.

- **`tradingagents/graph/trading_graph.py`**: The core of the application, where the `TradingAgentsGraph` class orchestrates the entire workflow. It uses `langgraph` to create a graph of agents that work together to analyze financial data and make trading decisions.

- **`tradingagents/default_config.py`**: Contains the default configuration for the application, including API keys, LLM settings, and market data provider preferences.

## Agents

The agents are the building blocks of the trading framework. They are organized into different teams based on their roles:

- **Analysts**: These agents are responsible for gathering and analyzing different types of data.
  - `fundamentals_analyst.py`: Analyzes the company's financial health.
  - `market_analyst.py`: Analyzes the overall market trends.
  - `news_analyst.py`: Analyzes the latest news and events.
  - `social_media_analyst.py`: Analyzes the sentiment on social media.

- **Managers**: These agents are responsible for managing the workflow and making high-level decisions.
  - `research_manager.py`: Manages the research process and synthesizes the findings of the researchers.
  - `risk_manager.py`: Manages the risk assessment process.

- **Researchers**: These agents are responsible for conducting in-depth research on specific topics.
  - `bull_researcher.py`: Focuses on the positive aspects of a stock.
  - `bear_researcher.py`: Focuses on the negative aspects of a stock.

- **Risk Management**: These agents are responsible for assessing the risks associated with a trade.
  - `aggresive_debator.py`: Takes an aggressive stance in the risk debate.
  - `conservative_debator.py`: Takes a conservative stance in the risk debate.
  - `neutral_debator.py`: Takes a neutral stance in the risk debate.

- **Trader**: This agent is responsible for making the final trading decision.
  - `trader.py`: Executes the trade based on the analysis and risk assessment.

## Dataflows

The `dataflows` directory contains the modules responsible for fetching data from different sources:

- **`data_source_manager.py`**: Manages the selection of data sources based on the market and the availability of the data.
- **`akshare_utils.py`**: Utility functions for fetching data from `akshare`, the primary source for A-share (Chinese market) data.
- **`yfin_utils.py`**: Provides utility functions for fetching data from `yfinance`.
- **`finnhub_utils.py`**: Provides utility functions for fetching data from `finnhub`.
- **`openai_utils.py`**: Helper wrappers around OpenAI-style LLM APIs used by the US-stock pipeline.
- **`interface.py`**: Provides a unified interface for accessing data from different sources.

## Multi-Market Routing

Starting from v0.4 the framework supports both US and A-share markets with automatic routing:

1. **Ticker Detection** – `Toolkit.ticker_is_china_stock()` determines whether a ticker belongs to the Chinese mainland exchanges (suffix `.SH`/`.SZ`).
2. **Routed Toolkit** – Core data accessors such as `Toolkit.get_fundamentals()` transparently dispatch to either `akshare_utils` (A-share) or the original OpenAI/Finnhub/SimFin back-ends (US stock).
3. **Agent Awareness** – Analyst nodes (`market_analyst.py`, `fundamentals_analyst.py`, etc.) query the toolkit only; they no longer need to know which market the ticker belongs to.
4. **Extensibility** – Adding support for a new market only requires implementing matching functions in `dataflows/<provider>_utils.py` and registering them in `Toolkit`.

## LLM Integration

The `LLM_INTEGRATION_GUIDE.md` file provides detailed instructions on how to integrate different LLMs with the application.