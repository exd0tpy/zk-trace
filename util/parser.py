import json
import requests

search_signature_global = False
address_shurink_global = True
return_value_global = True
data_shurink_global = True
ignore_hash_global = False
ignore_system_contract_global = False

system_contract_addr = dict()
with open("./data/system_contract_address.json", "r") as f:
    system_contract_addr = json.load(f)

def fetch_signature(signature):
    #return None
    if signature == '0x00000000':
        return None
    response = requests.get(f"https://api.etherface.io/v1/signatures/hash/all/{signature}/1")
    if response.status_code == 200:
        return response.json()['items'][0]['text']
    else:
        return None

def save_signature_to_file(signature, function_name):
    try:
        # 기존의 데이터를 읽어옴
        with open('./data/signature_info.json', 'r') as file:
            existing_data = json.load(file)
    except:
        # 파일이 없거나 JSON 파싱 에러가 발생한 경우 새로운 데이터로 시작
        existing_data = {}

    # 새로운 데이터를 추가
    if signature not in existing_data:
        existing_data[signature] = function_name

    # 데이터를 다시 파일에 저장
    with open('./data/signature_info.json', 'w') as file:
        json.dump(existing_data, file)


def get_function_name_from_file_or_fetch(signature):
    try:
        # signature_info.json 파일에서 데이터 읽기 시도
        with open('./data/signature_info.json', 'r') as file:
            data = json.load(file)
            # 최신 데이터를 반환
            return data[signature]
    except:
        # 파일이 없거나 JSON 파싱 에러가 발생한 경우 웹에서 데이터 가져오기
        fetched_data = fetch_signature(signature)
        # if fetched_data:
        save_signature_to_file(signature, fetched_data)
        return fetched_data

def isSystemContract(address):
    address_int = int(address, 16)
    if address_int == 0:
        return False
    return 0xffff > address_int


def parse_call(call, mermaid_list):
    if(not call):
        return

    from_address_original = call["from"]
    to_address_original = call["to"]
    
    input_data_original = call["input"]
    output_data_original = call["output"]

    function_signature = input_data_original[:10]

    input_data = input_data_original
    output_data = output_data_original
    function_name = ''

    from_address = from_address_original
    to_address = to_address_original

    entry_mark = False
    # Handle address
    if address_shurink_global:
        from_address = address_shurink(from_address_original)
        to_address = address_shurink(to_address_original)

    # Handle input & output
    if data_shurink_global:
        input_data = input_data_original[:2+8+64]
    if data_shurink_global:
        output_data = output_data_original[:2+64]

    # Handle function name
    if search_signature_global:
        function_name = get_function_name_from_file_or_fetch(function_signature)

    if function_name:
        input_data = function_name + ':' + input_data
    

    # Handle call function
    if not ignore_system_contract_global or not isSystemContract(to_address_original):
        if not ignore_hash_global or (to_address_original != "0x0000000000000000000000000000000000008010"):
            mermaid_list.append(f"{from_address}->>{to_address}: {input_data}")
            mermaid_list.append(f"activate {to_address}")


    for sub_call in call["calls"]:
        parse_call(sub_call, mermaid_list)

    if not ignore_system_contract_global or not isSystemContract(to_address_original):
        if not ignore_hash_global or (to_address_original != "0x0000000000000000000000000000000000008010"):
            if (return_value_global and (output_data != '0x')):
                mermaid_list.append(f"{to_address}->>{from_address}: {output_data}")
            mermaid_list.append(f"deactivate {to_address}")

def generate_mermaid(json_data):
    mermaid_list = ["sequenceDiagram"]
    parse_call(json_data, mermaid_list)
    return "\n".join(mermaid_list)

def address_shurink(address):
    if address in system_contract_addr:
        return system_contract_addr[address]
    return address[:6] + '...' + address[-4:]

def parse(json_data, search_signature=True, address_shurink=True, data_shurink=True, return_value=True, ignore_hash=True, ignore_system_contract=False):
    global search_signature_global, address_shurink_global, return_value_global, data_shurink_global, ignore_hash_global, ignore_system_contract_global

    search_signature_global = search_signature
    address_shurink_global = address_shurink
    return_value_global = return_value
    data_shurink_global = data_shurink
    ignore_hash_global = ignore_hash
    ignore_system_contract_global = ignore_system_contract

    return generate_mermaid(json_data)

# if __name__ == "__main__":
#     with open("simple_call.json", "r") as f:
#         data = json.load(f)
#     mermaid_syntax = generate_mermaid(data)
#     print(mermaid_syntax)
