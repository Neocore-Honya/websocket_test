from websocket import create_connection, enableTrace
import json

enableTrace(True)

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
        ws = create_connection(endpoint)
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