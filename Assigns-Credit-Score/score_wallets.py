import json
import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict

def timestamp_to_datetime(ts):
    return pd.to_datetime(ts, unit='s')

def compute_usd_value(row):
    try:
        amount = float(row['actionData'].get('amount', 0))
        price = float(row['actionData'].get('assetPriceUSD', 0))
        return (amount / 1e6) * price  # assuming 6 decimal places (e.g., USDC)
    except:
        return 0.0

def load_and_score(json_path):
    with open(json_path, 'r') as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)
    df['timestamp'] = df['timestamp'].apply(timestamp_to_datetime)
    df['usd_value'] = df.apply(compute_usd_value, axis=1)

    wallet_groups = df.groupby('userWallet')
    scores = {}

    for wallet, group in wallet_groups:
        total_txns = len(group)
        total_usd = group['usd_value'].sum()
        avg_usd = group['usd_value'].mean()
        std_usd = group['usd_value'].std()
        active_days = group['timestamp'].dt.date.nunique()
        last_active_days_ago = (datetime.utcnow() - group['timestamp'].max().to_pydatetime()).days
        unique_protocols = group['protocol'].nunique()
        unique_actions = group['action'].nunique()

        # Heuristic scoring model (0–1000)
        score = (
            total_txns * 2 +
            min(total_usd / 100, 200) +
            unique_protocols * 20 +
            unique_actions * 10 +
            (100 - min(last_active_days_ago, 100)) * 2 +
            active_days * 5
        )

        score = int(np.clip(score, 0, 1000))
        scores[wallet] = score

    return scores

if __name__ == "__main__":
    scores = load_and_score("User_Wallet_tran.json")

    # Print to console
    for wallet, score in scores.items():
        print(f"{wallet}: {score}")

    # Save to CSV
    output_df = pd.DataFrame(list(scores.items()), columns=["Wallet", "Score"])
    output_df.to_csv("wallet_scores.csv", index=False)
    print("\n✅ Wallet scores saved to wallet_scores.csv")

