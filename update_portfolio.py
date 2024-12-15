import os
import subprocess
import pandas as pd
import yfinance as yf
import datetime

# Function to fetch stock data
def fetch_stock_data(stock_list):
    today = datetime.datetime.today()
    start_date = today - datetime.timedelta(days=270)  # Approx. 9 months

    stock_data = []
    for stock in stock_list:
        try:
            data = yf.download(stock, start=start_date, end=today)
            data['Stock'] = stock
            data['7_Day_Avg'] = data['Adj Close'].rolling(window=7).mean()
            data['1_Month_Avg'] = data['Adj Close'].rolling(window=30).mean()
            data['3_Month_Avg'] = data['Adj Close'].rolling(window=90).mean()
            data['9_Month_Avg'] = data['Adj Close'].rolling(window=270).mean()
            latest = data.iloc[-1]
            stock_data.append({
                "Stock": stock,
                "Close": latest['Adj Close'],
                "7_Day_Avg": latest['7_Day_Avg'],
                "1_Month_Avg": latest['1_Month_Avg'],
                "3_Month_Avg": latest['3_Month_Avg'],
                "9_Month_Avg": latest['9_Month_Avg']
            })
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
    return pd.DataFrame(stock_data)

# Function to generate the HTML file
def generate_html(data, filename="index.html"):
    html_content = data.to_html(index=False, justify="center", border=1)
    with open(filename, "w") as file:
        file.write("<html><head><title>Stock Portfolio</title></head><body>")
        file.write("<h1>Stock Portfolio</h1>")
        file.write(html_content)
        file.write("</body></html>")
    print(f"HTML file '{filename}' created successfully.")

# Function to push to GitHub
def push_to_github(repo_path, commit_message):
    try:
        os.chdir(repo_path)  # Change to the repository directory
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to GitHub: {e}")

# Main function
if __name__ == "__main__":
    # Replace this with your local GitHub repo path
    repo_path = r"C:\\Users\\zainq\\stonks"

    # Replace with the stock symbols you own
    stocks = ["AAPL", "GOOGL", "MSFT"]

    # Fetch stock data
    stock_df = fetch_stock_data(stocks)

    # Add your shares and calculate portfolio value
    shares = {"AAPL": 10, "GOOGL": 5, "MSFT": 7}  # Example shares
    stock_df["Shares"] = stock_df["Stock"].map(shares)
    stock_df["Value"] = stock_df["Close"] * stock_df["Shares"]

    # Generate HTML file in the repo directory
    html_file = os.path.join(repo_path, "index.html")
    generate_html(stock_df, filename=html_file)

    # Commit and push to GitHub
    push_to_github(repo_path, "Update stock portfolio data")
