import time
import json
import players_pb2
import players_pb2_grpc
import redis
import grpc

#lee los summonerids del archivo
def read_summoner_ids_from_file(filename):
    with open(filename, 'r') as file:
        summoner_ids = [line.strip() for line in file]
    return summoner_ids

#obtener estadísticas de un jugador desde gRPC
def get_player_stats(summoner_id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = players_pb2_grpc.PlayersStub(channel)
        player_request = players_pb2.PlayerRequest(summonerid=summoner_id)
        player = stub.GetPlayer(player_request)
        return player

#conectar redis
redis_client = redis.StrictRedis(host='localhost', port=1337, db=0)

#obtener estadísticas en caché
def get_cached_stats(summoner_id):
    cached_data = redis_client.get(summoner_id)
    if cached_data:
        return cached_data
    return None

#guardar estadísticas en caché
def cache_stats(summoner_id, player_stats):
    redis_client.set(summoner_id, player_stats)

#funcion que simula una apirest
def get_stats(summoner_id):
    cached_stats = get_cached_stats(summoner_id)
    if cached_stats:
        return
    
    try:
        player_stats = get_player_stats(summoner_id)
        data = {
            'summonerid': player_stats.summonerid,
            'summonername': player_stats.summonername,
            'tier': player_stats.tier,
            'wins': player_stats.wins,
            'losses': player_stats.losses,
            'lp': player_stats.lp
        }

        cache_stats(summoner_id, json.dumps(data))

    except grpc.RpcError as e:
        print({'error': 'Error al comunicarse con el servidor gRPC'})

#funcion que calcula el tiempo de ejecución de get_stats() para cada summonerid
def calculate_execution_time(summoner_id):
    start_time = time.time()
    get_stats(summoner_id)
    end_time = time.time()
    return end_time - start_time

def main():
    summoner_ids = read_summoner_ids_from_file('random_summonerids.txt')
    total = 0
    i = 0
    for summoner_id in summoner_ids:
        execution_time = calculate_execution_time(summoner_id)
        total += execution_time
        i += 1
        if i % 1000 == 0:
            print(f'Summonerids procesados: {i}/{len(summoner_ids)}')
            print(f'Tiempo promedio de ejecución: {total / i:.5f} segundos')

    print(f'Tiempo total de ejecución: {total:.5f} segundos')

if __name__ == "__main__":
    main()