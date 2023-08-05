Running witness-node
####################

    ~/BitShares/bitshares-2
    programs/witness_node/witness_node --rpc-endpoint=127.0.0.1:8090

Running cli-wallet
##################

    ./programs/cli_wallet/cli_wallet -s ws://127.0.0.1:8090 -H 127.0.0.1:8092

Installation of python-graphene
###############################

    pip3 install graphenelib --user

or 

    git clone https://github.com/xeroc/python-graphenelib
    cd python-graphenelib
    make install-user

Connecting with cli-wallet and calling methods
##############################################
http://docs.bitshares.eu/api/wallet-api.html

    from grapheneapi.grapheneclient import GrapheneClient
    from grapheneapi.graphenewsprotocol import GrapheneWebsocketProtocol
    from pprint import pprint

    class Config(GrapheneWebsocketProtocol):
        wallet_host           = "localhost"
        wallet_port           = 8092

    if __name__ == '__main__':
        client = GrapheneClient(Config)
        pprint(client.getObject("2.0.0"))
        pprint(client.rpc.get_object("2.0.0"))
        account = client.rpc.get_account("fabian-secured")
        pprint(account)
        print(account["name"])

connecting with witness-node and calling method (database api and others)
#########################################################################
http://docs.bitshares.eu/api/database.html

    from grapheneapi.grapheneclient import GrapheneClient
    import json
    from pprint import pprint
    from datetime import datetime
    import time

    def formatTimeFromNow(secs=0):
        return datetime.utcfromtimestamp(time.time() + int(secs)).strftime('%Y-%m-%dT%H:%M:%S')

    class Config():
        wallet_host           = "localhost"
        wallet_port           = 8092
        witness_url           = "ws://localhost:8090/"

    if __name__ == '__main__':
        client = GrapheneClient(Config)
        pprint(client.ws.get_objects(["2.0.0"]))
        pprint(client.ws.get_full_accounts([account["id"]], False))
        pprint(client.ws.get_market_history("1.3.590",
                                            "1.3.0",
                                            24 * 60 * 60,
                                            formatTimeFromNow(-24 * 60 * 60),
                                            formatTimeFromNow(),
                                            api="history"
                                            ))

connecting with witness-node and running continuously
#####################################################

    from grapheneapi.grapheneclient import GrapheneClient
    from grapheneapi.graphenewsprotocol import GrapheneWebsocketProtocol
    import json
    from pprint import pprint


    class Config(GrapheneWebsocketProtocol):
        wallet_host           = "localhost"
        wallet_port           = 8092
        wallet_user           = ""
        wallet_password       = ""

        # witness_url           = "ws://localhost:8090/"
        witness_url           = "ws://10.0.0.16:8090/"
        witness_user          = ""
        witness_password      = ""

        def onRegisterHistory(self):
            print("Registered to history!")
        def onRegisterDatabase(self):
            print("Registered to database!")
        def onAccountUpdate(self, data):
            pprint(data)
        def onMarketUpdate(self, data):
            pprint(data)
        def onBlock(self, data) :
            pprint(data)

    if __name__ == '__main__':
        graphene = GrapheneClient(Config)
        graphene.run()
