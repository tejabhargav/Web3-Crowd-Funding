from brownie import contract1,contract2,UpgradeableProxy,ProxyAdmin,config,network,Contract
from scripts.helpful_scripts import get_account,encode_function_data,upgrade

def main():
    account=get_account()
    print(f"Deploying to {network.show_active()}")
    contract = contract1.deploy(
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    
    proxy_admin = ProxyAdmin.deploy(
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    
    contract_encoded_initializer_function = encode_function_data()
    
    proxy = UpgradeableProxy.deploy(
        contract.address,
        proxy_admin.address,
        contract_encoded_initializer_function,
        {"from":account, "gas_limit": 1000000},
        publish_source = config["networks"][network.show_active()].get("verify",False), 
    )
    
    print(f"Proxy deployed at {proxy.address}, upgrade to v2 now available")
    
    proxy_contract = Contract.from_abi("contract1", proxy.address, contract1.abi)
    print(f"proxy contract value:{proxy_contract.getValue()}")
    
    contract_2= contract2.deploy(
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify",False),
    )
    
    upgrade_tx = upgrade(account, proxy,contract_2,proxy_admin_contract=proxy_admin)
    upgrade_tx.wait(1)
    print(f"proxy upgraded to v2")
    
    proxy_contract_2 = Contract.from_abi("contract2",proxy.address , contract2.abi)
    print(f"proxy contract value : {proxy_contract_2.getValue()} ")
    
    tx= proxy_contract_2.setValue(22,{"from":account})
    tx.wait(1)
    
    print(f"proxy contract value : {proxy_contract_2.getValue()} ")