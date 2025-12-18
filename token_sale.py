from web3 import Web3
import json
import time

# Alchemy RPC URL provided
rpc_url = "https://eth-mainnet.g.alchemy.com/v2/FvrPNBGRAA9Nbh4-PpFdo4NSDrGxcv1W"

# GensynSale contract address (verified from Etherscan/Blockscan as the deployed GensynSale contract)
contract_address = "0x73612914c81a9c072333ea9ea71a9b26a5b9a707"

# Minimal ABI for the required view functions
abi = [
    {
        "inputs": [],
        "name": "numCommitters",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "committerAt",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "committer", "type": "address"}],
        "name": "committerStateByAddress",
        "outputs": [
            {"internalType": "address", "name": "addr", "type": "address"},
            {"internalType": "bytes16", "name": "entityID", "type": "bytes16"},
            {"internalType": "uint32", "name": "bidTimestamp", "type": "uint32"},
            {"internalType": "bool", "name": "cancelled", "type": "bool"},
            {"internalType": "bool", "name": "refunded", "type": "bool"},
            {
                "components": [
                    {"internalType": "contract IERC20", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "internalType": "struct GensynSale.TokenAmount[2]",
                "name": "acceptedAmountByToken",
                "type": "tuple[2]"
            },
            {
                "components": [
                    {"internalType": "uint64", "name": "price", "type": "uint64"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bool", "name": "lockup", "type": "bool"}
                ],
                "internalType": "struct GensynSale.Bid",
                "name": "currentBid",
                "type": "tuple"
            },
            {
                "components": [
                    {"internalType": "contract IERC20", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "internalType": "struct GensynSale.TokenAmount[2]",
                "name": "committedAmountByToken",
                "type": "tuple[2]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Connect to Ethereum via Alchemy
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum node")

# Create contract instance
contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

# Fetch number of committers
num_committers = contract.functions.numCommitters().call()
print(f"Total committers: {num_committers}")

# List to store results
committers_list = []

# Batch size to avoid overwhelming RPC (optional, but good for large numbers)
batch_size = 50
for start in range(0, num_committers, batch_size):
    end = min(start + batch_size, num_committers)
    print(f"Fetching committers {start} to {end - 1}...")

    for i in range(start, end):
        try:
            addr = contract.functions.committerAt(i).call()
            state = contract.functions.committerStateByAddress(addr).call()

            total_amount = state[6][1]  # currentBid.amount (index 6 is currentBid tuple, [1] is amount)
            usdc_amount = state[7][0][1]  # committedAmountByToken[0].amount (usually USDC)
            usdt_amount = state[7][1][1]  # committedAmountByToken[1].amount (usually USDT)
            price = state[6][0]  # currentBid.price
            lockup = state[6][2]  # currentBid.lockup

            committers_list.append({
                "address": addr,
                "total_usd_amount": total_amount / 1e6,  # Amounts are in 6 decimals (USDC/USDT style)
                "usdc_amount": usdc_amount / 1e6,
                "usdt_amount": usdt_amount / 1e6,
                "price": price,
                "lockup": lockup
            })
        except Exception as e:
            print(f"Error fetching committer at index {i}: {e}")

    # Small delay to be gentle on RPC
    time.sleep(0.5)

# Sort by total amount descending (optional)
committers_list.sort(key=lambda x: x["total_usd_amount"], reverse=True)

# Print results
print("\nList of committers (sorted by total amount descending):")
for c in committers_list[:50]:
    print(f"Address: {c['address']}")
    print(f"  Total USD: ${c['total_usd_amount']:,.2f}")
    print(f"  USDC: ${c['usdc_amount']:,.2f} | USDT: ${c['usdt_amount']:,.2f}")
    print(f"  Price: {c['price']} | Lockup: {c['lockup']}\n")

# Optional: Save to CSV
import csv

with open('gensyn_committers.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f,
                            fieldnames=["address", "total_usd_amount", "usdc_amount", "usdt_amount", "price", "lockup"])
    writer.writeheader()
    writer.writerows(committers_list)

print(f"Saved {len(committers_list)} committers to gensyn_committers.csv")
