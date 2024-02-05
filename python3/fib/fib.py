import timeit

def fibonacci(n: int) -> int:
    """Compute the nth value of the Fibonacci sequence."""
    if n < 0:
        raise ValueError('n cannot be negative')

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_with_memo(n: int, memo: dict[int, int] = {}) -> int:
    if n < 0:
        raise ValueError('n cannot be negative')

    if n < 2:
        return n

    if n not in memo:
        memo[n] = fibonacci_with_memo(n - 1, memo) + fibonacci_with_memo(n - 2, memo)

    return memo[n]


def fibonacci_time(n: int, repeat: int):
    SETUP = '''from __main__ import fibonacci'''
    TEST = f'fibonacci({n})'

    times = timeit.repeat(setup=SETUP,
                          stmt=TEST,
                          repeat=repeat,
                          number=1)
    print(f'Fibonacci times:            {times}')


def fibonacci_with_memo_time(n: int, repeat: int):
    SETUP = '''from __main__ import fibonacci_with_memo'''
    TEST = f'fibonacci_with_memo({n})'

    times = timeit.repeat(setup=SETUP,
                          stmt=TEST,
                          repeat=repeat,
                          number=1)
    print(f'Fibonacci with memo times:  {times}')


if __name__ == '__main__':
    n = 30
    repeat = 1
    fibonacci_time(n, repeat) # ~30 seconds
    fibonacci_with_memo_time(n, repeat) # ~0.00001 seconds
