import random
import simpy

N_CUSTOMERS = 20  # Total number of customers
MEAN_CUSTOMER_ARRIVAL = 10.0  # Generate new customers roughly every x seconds

n_served = 0
n_balked = 0

class Customer:
    def __init__(self, env: simpy.Environment, id: int, mean_patience: float, mean_time_in_bank: float):
        self.env = env
        self.id = id
        self.arrival_time = env.now
        self.patience = random.expovariate(1.0 / mean_patience)
        self.time_in_bank = random.expovariate(1.0 / mean_time_in_bank)
        print(f"{self.arrival_time:7.2f}: {self} arrived")

    def serve(self, counter: simpy.Resource):
        global n_served, n_balked
        with counter.request() as request:
            results = yield request | self.env.timeout(self.patience)
            wait_time = self.env.now - self.arrival_time
            if request in results:
                print(f"{self.env.now:7.2f}: {self} starts being served")
                yield self.env.timeout(self.time_in_bank)
                print(f"{self.env.now:7.2f}: {self} finished being served (time in bank: {self.time_in_bank:.2f} minutes)")
                n_served += 1
            else:
                print(f"{self.env.now:7.2f}: {self} balked at after waiting {wait_time:.2f} minutes")
                n_balked += 1

    def __repr__(self) -> str:
        return f"Customer {self.id}"


def setup(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)
        c = Customer(env, i, mean_patience=4.0, mean_time_in_bank=12.0)
        env.process(c.serve(counter))

# Setup and start the simulation
print("Starting simulation")
# random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(setup(env, N_CUSTOMERS, MEAN_CUSTOMER_ARRIVAL, counter))
env.run()

print(f"Total number of customers: {N_CUSTOMERS}, served: {n_served}, balked: {n_balked}")
