# EconAnalysisBot
## A tool for analyzing economic data to aid investment decisions

This bot was made to simplify the process of investment decisions and analysis of companies, which is very complex and technical.

This bot uses Selenium to webscrape through the website br.investing.com to collect data on all the companies of the Brazilian stock exchange to produce financial analysis on a company's financial situation.
After all the data is collected, it is fed into the GCP LLM (gemini) to synthesise a simpler analysis of the company's financial health, which even produces a conclusion, based on a predefined prompt.
