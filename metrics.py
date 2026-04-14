import time

def measure_latency(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, round(end - start, 3)
    return wrapper


def evaluate_retrieval(scores):
    if not scores:
        return 0

    # proxy: higher similarity → better retrieval
    return round(max(scores), 3)


def evaluate_answer(answer):
    return {
        "length": len(answer.split()),
        "has_content": len(answer.strip()) > 0
    }