import requests
from util import argument_setting
from util import parser

def get_raw_trace(rpc_url, txHash):
    data = f'''{{
      "jsonrpc": "2.0",
      "id": "2",
      "method": "debug_traceTransaction",
      "params": [
        "{txHash}",
        {{ "tracer": "callTracer", "tracerConfig": {{ "onlyTopCall": false }} }}
      ]
    }}'''
    result = requests.post(rpc_url, headers={'content-type': 'application/json'}, data=data)
    return result.json()

def getEntryCall(call_data):
    first = call_data
    found = False
    entry_call = {}
    if(not parser.isSystemContract(call_data['from']) and not parser.isSystemContract(call_data['to'])):
        return call_data
    for c in call_data['calls']:
        temp = getEntryCall(c)
        if(temp):
            entry_call = temp
            return entry_call
    return entry_call
  
def execute(rpc_url, tx_hash, options):
    raw_trace = get_raw_trace(rpc_url, tx_hash)

    entry_call = raw_trace["result"]
    if options["skip_bootloader"]:
      entry_call = getEntryCall(raw_trace["result"])
    del(options["skip_bootloader"])
    #print(parser.parse(entry_call, search_signature=args.signature_search, address_shurink=args.short_address, data_shurink=args.short_data, return_value=args.ignore_return_value, ignore_hash=args.ignore_hash, ignore_system_contract=args.ignore_system_contract))
    return parser.parse(entry_call, **options)

def main():
    args = argument_setting.get_args()
    print(args)
    # Get raw trace data
    #raw_trace = get_raw_trace('https://testnet.era.zksync.dev', '0x267855e5736eeb3c3da61158f34ab602ae1ceba6fa020487d95a55b44acb8f1a')
    raw_trace = get_raw_trace(args.rpc_url, args.tx_hash)

    entry_call = raw_trace["result"]
    if args.skip_bootloader:
      entry_call = getEntryCall(raw_trace["result"])

    options_ = {
      'search_signature': args.signature_search,
      'address_shurink': args.short_address,
      'data_shurink': args.short_data,
      'ignore_hash': args.ignore_hash,
      'return_value': args.ignore_return_value,
      'ignore_system_contract': args.ignore_system_contract,
    }
    #print(parser.parse(entry_call, search_signature=args.signature_search, address_shurink=args.short_address, data_shurink=args.short_data, return_value=args.ignore_return_value, ignore_hash=args.ignore_hash, ignore_system_contract=args.ignore_system_contract))
    print(parser.parse(entry_call, **options_))
if __name__ == "__main__":
    main()

