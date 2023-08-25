import random
import simpy

MEAN_ARRIVAL = 3.0
SIM_DURATION = 120.0

counter = 0

def arrivals(env, mean):
    global counter
    while True:
        counter += 1
        next_arrival = random.expovariate(1.0 / mean)
        print(f"{env.now:.2f}: Arrival {counter}")
        yield env.timeout(next_arrival)

print("Start")
env = simpy.Environment()
env.process(arrivals(env, MEAN_ARRIVAL))
env.run(until=SIM_DURATION)
print(f"Done. There were {counter} arrivals in {SIM_DURATION} minutes.")
