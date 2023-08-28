import random
import simpy

SIM_DURATION = 100
MEAN_INTERVAL = 5.0
MEAN_DELIVERY_DELAY = 10.0

class Message:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return f"Message({self._id})"


class Cable:
    def __init__(self, env: simpy.Environment, mean_delivery_delay: float):
        self._env = env
        self._delay = random.expovariate(1.0 / mean_delivery_delay)
        self._store = simpy.Store(env)

    def latency(self, message: Message):
        yield self._env.timeout(self._delay)
        return self._store.put(message)

    def put(self, message: Message):
        self._env.process(self.latency(message))

    def get(self):
        return self._store.get()


class Sender:
    def __init__(self, env):
        self._env = env

    def send(self, cable: Cable, mean_interval: float):
        counter = 0
        while True:
            yield self._env.timeout(random.expovariate(1.0 / mean_interval))
            counter += 1
            message = Message(counter)
            cable.put(message)
            print(f"{self._env.now:8.2f}: sent message {message}")


class Receiver:
    def __init__(self, env):
        self._env = env

    def receive(self, cable: Cable):
        while True:
            message = yield cable.get()
            print(f"{self._env.now:8.2f}: received message {message}")


print('Start event latency demo')

env = simpy.Environment()
sender = Sender(env)
receiver = Receiver(env)
cable = Cable(env, MEAN_DELIVERY_DELAY)

env.process(sender.send(cable, MEAN_INTERVAL))
env.process(receiver.receive(cable))

env.run(until=SIM_DURATION)
