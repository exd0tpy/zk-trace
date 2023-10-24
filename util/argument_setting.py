import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Call tracer & visualizer for zksync")

    parser.add_argument("tx_hash", type=str, help="transaction hash to trace")
    parser.add_argument("rpc_url", type=str, help="request rpc address")


    # 선택 가능한 인자
    parser.add_argument("--signature-search", action="store_true", help="enable signature search")
    parser.add_argument("--short-address", action="store_true", help="shurink address")
    parser.add_argument("--short-data", action="store_true", help="show only 1 slot of data")
    parser.add_argument("--ignore-hash", action="store_false", help="not print keccak256 call")
    parser.add_argument("--ignore-return-value", action="store_false", help="not print return value")
    parser.add_argument("--ignore-system-contract", action="store_false", help="not print system contract")
    parser.add_argument("--skip-bootloader", action="store_true", help="remove bootloader process")
    
    args = parser.parse_args()

    return args
