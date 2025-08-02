import json
import pandas as pd
from datetime import datetime
import numpy as np

def load_wallet_features(json_path):
    with open(json_path, 'r') as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    def compute_usd(row):
        try:
            amt = float(row['actionData'].get('amount', 0))
            price = float(row['actionData'].get('assetPriceUSD', 0))
            return (amt / 1e6) * price
        except:
            return 0.0

    df['usd_value'] = df.apply(compute_usd, axis=1)

    features = []

    for wallet, group in df.groupby("userWallet"):
        total_txns = len(group)
        total_usd = group["usd_value"].sum()
        avg_usd = group["usd_value"].mean()
        std_usd = group["usd_value"].std()
        active_days = group["timestamp"].dt.date.nunique()
        last_days = (datetime.utcnow() - group["timestamp"].max().to_pydatetime()).days
        actions = group['action'].value_counts(normalize=True)

        features.append({
            "userWallet": wallet,
            "total_txns": total_txns,
            "total_usd": total_usd,
            "avg_usd_value": avg_usd,
            "std_usd_value": std_usd,
            "active_days": active_days,
            "last_txn_days_ago": last_days,
            "borrow_ratio": actions.get("borrow", 0),
            "repay_ratio": actions.get("repay", 0),
            "deposit_ratio": actions.get("deposit", 0),
            "redeem_ratio": actions.get("redeemunderlying", 0),
            "liquidation_ratio": actions.get("liquidationcall", 0),
            "unique_actions": group["action"].nunique()
        })

    return pd.DataFrame(features)

def generate_synthetic_score(features_df):
    """
    Generates a synthetic score between 0-1000 based on existing features.
    """
    def score_fn(row):
        score = 0

        # 🟢 Positive behavior
        score += min(row['deposit_ratio'] * 500, 150)  # More deposits = better
        score += min(row['repay_ratio'] * 500, 150)    # More repayments = better
        score += min(row['active_days'] * 2, 100)      # More active days = better
        score += min(row['avg_usd_value'] / 100, 100)  # Larger avg txn = better
        score += min(row['unique_actions'] * 10, 100)  # Diversity of actions

        # 🔴 Risky behavior
        score -= min(row['borrow_ratio'] * 500, 100)   # Too much borrowing
        score -= min(row['liquidation_ratio'] * 500, 100)  # Liquidations = bad
        score -= min(row['last_txn_days_ago'], 50)     # Inactive users = risky

        return max(0, min(int(score), 1000))

    features_df['credit_score'] = features_df.apply(score_fn, axis=1)
    return features_df

if __name__ == "__main__":
    df = load_wallet_features("User_Wallet_tran.json")  # replace with correct path if needed
    features_with_scores = generate_synthetic_score(df)
    print(features_with_scores.head())

    features_with_scores.to_csv("wallet_features_with_scores.csv", index=False)
    print("✅ Features + synthetic credit scores saved to CSV!")
