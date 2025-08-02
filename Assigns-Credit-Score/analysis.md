# 📊 Credit Score Analysis Report

## 🔢 Score Distribution
Distribution of wallet credit scores across 100-point buckets:

score_range
(0, 100]        163
(100, 200]     1241
(200, 300]     1896
(300, 400]      150
(400, 500]       11
(500, 600]        0
(600, 700]        0
(700, 800]        0
(800, 900]        0
(900, 1000]       0

---
## 🟥 Behavior of Low-Scoring Wallets (0–300)
- Count: 3332
- Tend to have higher `borrow_ratio` and `liquidation_ratio`.
- Often inactive (`last_txn_days_ago` high).
- Fewer actions and low diversity.

## 🟩 Behavior of High-Scoring Wallets (700–1000)
- Count: 0
- High `deposit_ratio` and `repay_ratio`.
- Consistently active users (`active_days` high).
- Large average USD transaction values.
- Diverse interactions with protocol.
