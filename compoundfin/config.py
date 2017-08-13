
"""
Config values like DB name, bank accounts to query
This file should be a symlink to a private configuration file
"""

DB_NAME = "compound-dev"
# DB_NAME = "compound-prod"

# Matrix for currency conversation rates
# Rates are multiplicitive from higher to lower in the nesting
# For example, to convert CAD to USD,
# multiply the CAD amount by EXCHANGE_RATES["CAD"]["USD"]
EXCHANGE_RATES = {
        "CAD": {"CAD": 1.00, "USD": 0.80},
        "USD": {"CAD": 1.25, "USD": 1.00},
        }

time_format = '%Y-%m-%d'
