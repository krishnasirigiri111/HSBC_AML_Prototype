import pandas as pd
from sklearn.ensemble import IsolationForest
from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

# Load data
data = pd.read_csv('transactions.csv')

# Encrypt account IDs
data['account_encrypted'] = data['account'].apply(lambda x: cipher.encrypt(x.encode()).decode())

# Select features for anomaly detection
features = data[['amount']]

# Train Isolation Forest
model = IsolationForest(contamination=0.2, random_state=42)  # type: ignore[arg-type]  # linter false positive; float is valid
model.fit(features)

# Predict anomalies (-1 for anomalies, 1 for normal)
data['anomaly'] = model.predict(features)

# Save suspicious transactions
suspicious = data.loc[data['anomaly'] == -1, ['transaction_id', 'amount', 'account_encrypted', 'timestamp', 'location']]
assert hasattr(suspicious, 'to_csv'), "suspicious is not a DataFrame!"
suspicious.to_csv('suspicious_transactions.csv', index=False)
print("Suspicious Transactions:\n", suspicious)