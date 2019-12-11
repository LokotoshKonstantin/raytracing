import pstats
import cProfile


def profile(func):
    def wrapper(*args, **kwargs):
        profile_filename = "logs/" + func.__name__ + ".prof"
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper


def log2text(log_file: str):
    s = pstats.Stats(log_file).sort_stats("tottime")
    s.print_stats()
    return s.stats


if __name__ == "__main__":
    log = log2text("./rendering_per_pixel.prof")
