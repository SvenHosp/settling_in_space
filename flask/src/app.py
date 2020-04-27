from flask import Flask
app = Flask(__name__)

def get_rpc_methods():
    import xmlrpc.client

    with xmlrpc.client.ServerProxy("http://rpcgame:8082") as proxy:
        # Print list of available methods
        return proxy.system.listMethods()

@app.route('/')
def hello_world():
    rpc_methods = get_rpc_methods()
    text = 'rpc hat folgende Methoden zur Auswahl: {0}'.format(rpc_methods)
    return text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')