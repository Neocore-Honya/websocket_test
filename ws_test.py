from websocket import create_connection, enableTrace
import json
import ssl

enableTrace(True)

my_context = ssl.create_default_context()
try:
    print('loading cacert.pem')
    my_context.load_verify_locations('cacert.pem')
except:
    print('failed')

try:
    print('loading custom.pem')
    my_context.load_verify_locations('custom.pem')
except:
    print('failed')

try:
    print('loading custom.cer')
    my_context.load_verify_locations('custom.cer')
except:
    print('failed')

requestId = 1

def send_request( req, ws ):
    global requestId
    req['requestId'] = str(requestId)
    requestId = requestId + 1
    reqdata = json.dumps(req)
    print(">>> "+reqdata)
    ws.send(reqdata)
    result = ws.recv()
    print("<<< " + result)
    if result == '':
        return {}
    return json.loads(result)

def run_test(endpoint):
    global requestId
    requestId = 1

    try:
        print("connecting")
        ws = create_connection(endpoint,sslopt={'context':my_context})
        print("connected")

        try:
            print("sending initial handshake")
            send_request({'action':'handshake'},ws)
        except Exception as e:
            print('Exception: ', str(e))

        print("Closing connection")
        ws.close()
    except Exception as e:
        print('Exception: ', str(e))

print('Testing gamesparks')
run_test('wss://preview-v368622fnPKd.ws.gamesparks.net/ws/dedicatedServer/v368622fnPKd')

print('Testing AWS')
run_test('wss://iz0k29t5mh.execute-api.us-west-2.amazonaws.com/preview')

input("Press Enter to continue...")