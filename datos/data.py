import csv
import random
import string

#rangos del lol
tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]

data = []
for _ in range(3000000):
    summonerid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    summonername = ''.join(random.choices(string.ascii_letters, k=10))
    tier = random.choice(tiers)
    wins = random.randint(0, 1000)
    losses = random.randint(0, 1000)
    lp = random.randint(0, 100)
    data.append([summonerid, summonername, tier, wins, losses, lp])

csv_filename = "data.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Archivo CSV generado exitosamente:", csv_filename)
