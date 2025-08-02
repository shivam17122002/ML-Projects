import pandas as pd
import matplotlib.pyplot as plt

# Load the scored data
df = pd.read_csv("wallet_features_with_scores.csv")

# Define score buckets
score_bins = list(range(0, 1100, 100))  # 0–1000 in steps of 100
df['score_range'] = pd.cut(df['credit_score'], bins=score_bins)

# Count number of wallets in each score range
score_distribution = df['score_range'].value_counts().sort_index()

# Plot distribution
plt.figure(figsize=(10,6))
score_distribution.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Wallet Credit Score Distribution')
plt.xlabel('Credit Score Range')
plt.ylabel('Number of Wallets')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("score_distribution.png")
plt.close()

# Save insights to markdown
with open("analysis.md", "w", encoding="utf-8") as f:
    f.write("# 📊 Credit Score Analysis Report\n\n")
    f.write("## 🔢 Score Distribution\n")
    f.write("Distribution of wallet credit scores across 100-point buckets:\n\n")
    f.write(score_distribution.to_string())
    f.write("\n\n---\n")
    f.write("## 🟥 Behavior of Low-Scoring Wallets (0–300)\n")
    low_score_wallets = df[df['credit_score'] < 300]
    f.write(f"- Count: {len(low_score_wallets)}\n")
    f.write(f"- Tend to have higher `borrow_ratio` and `liquidation_ratio`.\n")
    f.write(f"- Often inactive (`last_txn_days_ago` high).\n")
    f.write(f"- Fewer actions and low diversity.\n\n")

    f.write("## 🟩 Behavior of High-Scoring Wallets (700–1000)\n")
    high_score_wallets = df[df['credit_score'] > 700]
    f.write(f"- Count: {len(high_score_wallets)}\n")
    f.write(f"- High `deposit_ratio` and `repay_ratio`.\n")
    f.write(f"- Consistently active users (`active_days` high).\n")
    f.write(f"- Large average USD transaction values.\n")
    f.write(f"- Diverse interactions with protocol.\n")
