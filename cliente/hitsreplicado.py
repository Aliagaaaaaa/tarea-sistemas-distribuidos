import time
import json
import players_pb2
import players_pb2_grpc
import redis
import grpc
import random
import threading

#lee los summonerids del archivo
def read_summoner_ids_from_file(filename):
    with open(filename, 'r') as file:
        summoner_ids = [line.strip() for line in file]
    return summoner_ids

#servidores redis
redis_ports = [1337, 1338, 1339]
redis_clients = [redis.StrictRedis(host='localhost', port=port, db=0) for port in redis_ports]

#funcion para obtener estadísticas en caché del servidor 'client'
def get_cached_stats(summoner_id, client):
    return client.get(summoner_id)

#funcion para almacenar estadísticas en caché del servidor '1337' (client[0])
def cache_stats(summoner_id, player_stats):
    redis_clients[0].set(summoner_id, player_stats)

#funcion para revisar si hubo un hit o miss en la caché(1 si hubo hit, 0 si hubo miss)
def get_stats(summoner_id, client):
    cached_stats = get_cached_stats(summoner_id, client)
    if cached_stats:
        return 1
    
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = players_pb2_grpc.PlayersStub(channel)
            player_request = players_pb2.PlayerRequest(summonerid=summoner_id)
            player = stub.GetPlayer(player_request)
            data = {
                'summonerid': player.summonerid,
                'summonername': player.summonername,
                'tier': player.tier,
                'wins': player.wins,
                'losses': player.losses,
                'lp': player.lp
            }
            cache_stats(summoner_id, json.dumps(data))
            return 0

    except grpc.RpcError as e:
        print({'error': 'Error al comunicarse con el servidor gRPC'})

# Función para calcular el tiempo de ejecución de get_stats() para cada summonerid
def calculate_hits(summoner_id, client):
    return get_stats(summoner_id, client)

def process_summoner_ids(summoner_ids, client):
    total = 0
    i = 0
    for summoner_id in summoner_ids:
        hit = calculate_hits(summoner_id, client)
        total += hit
        i += 1
        if i % 1000 == 0:
            print(f'Thread {client} - {i} summonerids procesados. Hits: {total}')

    print(f'Thread finalizado. Tiempo total: {total:.2f} segundos')

    return total

def main():
    summoner_ids = read_summoner_ids_from_file('random_summonerids.txt')
    num_summoner_ids = len(summoner_ids)
    chunk_size = num_summoner_ids // len(redis_clients)
    chunks = [summoner_ids[i:i+chunk_size] for i in range(0, num_summoner_ids, chunk_size)]

    threads = []
    for i, client in enumerate(redis_clients):
        thread = threading.Thread(target=process_summoner_ids, args=(chunks[i], client))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Todos los threads han finalizado.")

if __name__ == "__main__":
    main()