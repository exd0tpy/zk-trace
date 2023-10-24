# ZK-TRACE
Smart trace for zksync transaction.

## Feature
- Automatic function signature search
- Remove Bootloader process
- Ignore system contract logic
- Demo webapp

### Usage
`usage: tracer.py [-h] [--signature-search] [--short-address] [--short-data] [--ignore-hash] [--ignore-return-value] [--ignore-system-contract] [--skip-bootloader] tx_hash rpc_url`

### TODO
- [ ] Contract abi integration
    - [ ] Track function call arguments

