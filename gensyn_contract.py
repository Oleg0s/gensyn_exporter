from web3 import Web3
from GensynABI import ABI
from config import rpc_url
from peers import peers

class GensynContract:
    contract_address = Web3.to_checksum_address('0x7745a8FE4b8D2D2c3BB103F8dCae822746F35Da0')
    name = "New smart contract"
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=ABI)

    def getTotalRewards(self, peers):
        return self.contract.functions.getTotalRewards(peers).call()

    def getTotalWins(self, peer):
        return self.contract.functions.getTotalWins(peer).call()

    def currentStage(self):
        return self.contract.functions.currentStage().call()

    def getVoterVoteCount(self, peer):
        return self.contract.functions.getVoterVoteCount(peer).call()

class GensynOldContract(GensynContract):
    contract_address = Web3.to_checksum_address('0xFaD7C5e93f28257429569B854151A1B8DCD404c2')
    name = "Old smart contract"

if __name__ == "__main__":
    # for c in [GensynOldContract(), GensynContract()]:
    #     for f in c.contract.functions:
    #         print(f)
    #
    #     print(c.getVoterVoteCount("QmaYGPFSzLQwnFrpRi7gG68qiNmAcDF3obqUs415CXGUHU"))

    # # Rewards
    # for c in [GensynOldContract(), GensynContract()]:
    #     print(c.name)
    #     print("=" * 20)
    #     for peer in peers.keys():
    #         rewards = c.getTotalRewards(peers[peer])
    #         print(peer)
    #         for i in range(len(rewards)):
    #             print(f" ...{peers[peer][i][-4:]}: {rewards[i]}")
    #         print("-" * 20)

    # Participation
    for c in [GensynOldContract(), GensynContract()]:
        print(c.name)
        print("=" * 20)
        for group, g_peers in peers.items():
            print(f"{group}")
            for peer in g_peers:
                votes = c.getVoterVoteCount(peer) * 3
                print(f" ...{peer[-4:]}: {votes}")
            print("-" * 20)
