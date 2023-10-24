from flask import Flask, render_template, request, redirect, url_for
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


import tracer
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tx_hash = request.form.get('tx_hash')
        rpc_url = request.form.get('rpc_url')

        options = {
            'search_signature': request.form.get('signature_search'),
            'address_shurink': request.form.get('short_address'),
            'data_shurink': request.form.get('short_data'),
            'ignore_hash': request.form.get('ignore_hash'),
            'return_value': request.form.get('ignore_return_value'),
            'ignore_system_contract': request.form.get('ignore_system_contract'),
            'skip_bootloader': request.form.get('skip_bootloader')
        }
#print(parser.parse(entry_call, search_signature=args.signature_search, address_shurink=args.short_address, data_shurink=args.short_data, return_value=args.ignore_return_value, ignore_hash=args.ignore_hash, ignore_system_contract=args.ignore_system_contract))
        mermaid_data = tracer.execute(rpc_url, tx_hash, options)
        return render_template('mermaid.html', data=mermaid_data)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
