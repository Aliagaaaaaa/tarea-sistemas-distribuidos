import players_pb2
import players_pb2_grpc
import grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = players_pb2_grpc.PlayersStub(channel)

        print("-------------- GetPlayer --------------")
        player_request = players_pb2.PlayerRequest(summonerid='hfXaVys0L8s1y3I4Oyl1JFVz6FZ52u')
        player = stub.GetPlayer(player_request)
        print(player)

if __name__ == '__main__':
    run()
