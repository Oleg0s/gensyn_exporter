from web3 import Web3
from GensynABI import ABI
from config import rpc_url


from_block = 11185235
to_block = from_block + 5

# Contract address
contract_address = Web3.to_checksum_address('0x7745a8FE4b8D2D2c3BB103F8dCae822746F35Da0')

abi = ABI

# Connect to the node
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if not w3.is_connected():
    print("Failed to connect to the RPC endpoint.")
    exit()

# If ABI is provided, create a contract object for decoding
if abi:
    contract = w3.eth.contract(address=contract_address, abi=abi)
else:
    contract = None
    print("No ABI provided; outputting raw logs only.")

for f in contract.functions:
    print(f)
exit()

# Fetch logs (all historical from block 0 to latest)
logs = w3.eth.get_logs({
    'fromBlock': from_block,
    'toBlock': to_block,
    'address': contract_address
})

# Process and print logs
if not logs:
    print("No logs found for this contract.")
else:
    print(f"Found {len(logs)} logs:")
    for log in logs:
        # Decode if ABI and contract object are available
        if contract:
            try:
                # Decode the log using the contract's event ABI
                # decoded_log = contract.events[log['topics'][0].hex()]().process_log(log)
                decoded_log = contract.events["RewardSubmitted"]().process_log(log)
                print("\n--- Log ---")
                print(f"Block Number: {log['blockNumber']}")
                print(f"Transaction Hash: {log['transactionHash'].hex()}")

                print("Decoded Event:")
                print(f"Event Name: {decoded_log.event}")
                print("Parameters:")
                for key, value in decoded_log.args.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                # print(f"Failed to decode log: {e}")
                pass
