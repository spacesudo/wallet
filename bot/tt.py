import json

# Sample data
data = {
    "result": [
        {
            "hash": "0x1ed85b3757a6d31d01a4d6677fc52fd3911d649a0af21fe5ca3f886b153773ed",
            "nonce": "1848059",
            "transaction_index": "108",
            "from_address_entity": "Opensea",
            "from_address_entity_logo": "https://opensea.io/favicon.ico",
            "from_address": "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0",
            "from_address_label": "Binance 1",
            "to_address_entity": "Beaver Build",
            "to_address_entity_logo": "https://beaverbuild.com/favicon.ico",
            "to_address": "0x003dde3494f30d861d063232c6a8c04394b686ff",
            "to_address_label": "Binance 2",
            "value": "115580000000000000",
            "gas": "30000",
            "gas_price": "52500000000",
            "block_timestamp": "2021-05-07T11:08:35.000Z",
            "block_number": "12386788",
            "block_hash": "0x9b559aef7ea858608c2e554246fe4a24287e7aeeb976848df2b9a2531f4b9171",
        }
    ]
}

# Function to format and display data
def display_transaction_info(transaction):
    output = []
    
    # Formatting the result
    output.append("Transaction Details".center(50, "="))
    output.append(f"Transaction Hash: {transaction['hash']}")
    output.append(f"From: {transaction['from_address_entity']} ({transaction['from_address_label']})")
    output.append(f"To: {transaction['to_address_entity']} ({transaction['to_address_label']})")
    output.append(f"Value: {int(transaction['value']) / 1e18:.4f} ETH")
    output.append(f"Gas Used: {transaction['gas']}")
    output.append(f"Gas Price: {int(transaction['gas_price']) / 1e9:.2f} Gwei")
    output.append(f"Block Number: {transaction['block_number']}")
    output.append(f"Timestamp: {transaction['block_timestamp']}")
    output.append("=" * 50)
    
    return "\n".join(output)

# Extract transaction data
transaction_data = data["result"][0]

# Get formatted string
formatted_data = display_transaction_info(transaction_data)

# Print to console in fancy format
print(formatted_data)

# Save to file
with open("result.txt", "w") as file:
    file.write(formatted_data)

print("Results have been saved to result.txt")
