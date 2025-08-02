# Assigns-Credit-Score
# 💸 DeFi Wallet Credit Scoring

Ever wondered how trustworthy a wallet is on a DeFi platform? This project tackles exactly that — assigning a **credit score between 0 and 1000** to wallets interacting with the Aave V2 protocol. By analyzing their past behavior — deposits, borrows, repayments, liquidations — we predict how "healthy" or "risky" a user is.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🎯 Goal

Use raw transaction-level data to **build a behavior-based credit scoring system** for DeFi users. The higher the score, the more reliable the wallet.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧠 How It Works

We extract meaningful features from each wallet's transaction history (e.g., how often they borrow vs. repay, how much value they move, how active they are). Then we apply a scoring logic — or train a model — to evaluate them on a scale from 0 to 1000.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠️ Pipeline Overview

```plaintext
[Raw JSON Transactions]
        |
        v
[Feature Engineering] → [Wallet-Level Dataset with Scores] → [Model Training] (optional)
        |
        v
[Analysis Report + Visualizations]
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

## 🔍 What’s Inside

* \`\`: Parses wallet data & generates score features
* \`\`: Trains a Random Forest model on synthetic scores
* \`\`: Creates a visual + markdown analysis of score distributions
* \`\`: Input data (100K sample txns)
* \`\`: Cleaned + scored output
* \`\`: Trained model for reuse
* \`\`: Human-readable wallet behavior insights
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Getting Started

```bash
# Step 1: Create wallet features & scores
python ml_wallet_features_engineering.py

# Step 2: (Optional) Train model from scratch
python train_credit_model.py

# Step 3: Analyze results & visualize score distribution
python analyze_scores.py
```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🔬 Why It Matters

This system mimics traditional credit scoring — but in the DeFi world. It's useful for:

* Lending protocols
* Risk management tools
* Behavioral analytics for crypto wallets
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📊 Score Insight

We bucket scores in ranges (0–100, 100–200, ..., 900–1000) and analyze how wallets behave across them — bots, spammers, long-term users, whales, and everyone in between.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## ✅ Project Status

✔️ Fully functional
✔️ Model trained (or scoring function available)
✔️ Scalable and modular for other DeFi protocols

---

> 🔗 Feel free to fork, improve, or integrate into your own DeFi risk engine!
