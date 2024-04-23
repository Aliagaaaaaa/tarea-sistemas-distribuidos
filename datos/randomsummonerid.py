import psycopg2
import random

#no es necesario usar servidor gRPC
conn = psycopg2.connect(
    database="lmao",
    user="username",
    password="martin1337",
    host="34.176.189.166",
    port="5432"
)

cursor = conn.cursor()

n = 50000

cursor.execute("SELECT COUNT(*) FROM players")
total_rows = cursor.fetchone()[0]

cursor.execute("SELECT summonerid FROM players")
all_summonerids = [row[0] for row in cursor.fetchall()]
random_summonerids = random.sample(all_summonerids, n)

# duplicar y triplicar la mitad de los valores aleatorios
duplicates_count = int(0.5 * n)
triplicates_count = int(0.5* n)

selected_summonerids = []

for summonerid in random_summonerids:
    if duplicates_count > 0:
        selected_summonerids.extend([summonerid, summonerid])
        duplicates_count -= 1
    elif triplicates_count > 0:
        selected_summonerids.extend([summonerid, summonerid, summonerid])
        triplicates_count -= 1
    else:
        selected_summonerids.append(summonerid)

# Desordenar la lista de summonerids
random.shuffle(selected_summonerids)

# Guardar los 'summonerid' en un archivo de texto
with open("random_summonerids.txt", "w") as file:
    for summonerid in selected_summonerids:
        file.write(str(summonerid) + "\n")

conn.close()

print("Valores aleatorios desordenados y guardados en 'random_summonerids.txt'")
