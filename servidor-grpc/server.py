from concurrent import futures

import grpc
import players_pb2
import players_pb2_grpc

import psycopg2

conn = psycopg2.connect(
    database="lmao",
    user="username",
    password="martin1337",
    host="34.176.189.166",
    port="5432"
)

cur = conn.cursor()

class PlayersServicer(players_pb2_grpc.PlayersServicer):
    def GetPlayer(self, request, context):
        print("GetPlayer request received:", request)

        cur = conn.cursor()
        cur.execute("SELECT * FROM players WHERE summonerid = %s", (request.summonerid,))
        player = cur.fetchone()

        if player:
            return players_pb2.Player(
                summonerid=player[0],
                summonername=player[1],
                tier=player[2],
                wins=player[3],
                losses=player[4],
                lp=player[5]
            )
        
        return players_pb2.Player()
        

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    players_pb2_grpc.add_PlayersServicer_to_server(PlayersServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()
