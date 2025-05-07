import os

CPU_COUNT = os.cpu_count() or 1

#  program args default values
ARG_DEFAULT_MAX_THREADS: int = min(32, CPU_COUNT * 2)
ARG_DEFAULT_MIN_PATH_LEN: int = 2

# validation values
SAFEGUARD_THRESHOLD_COMPLEXITY: int = (10 ** 5) * 3  # protect from excessive computation and output files
SAFEGUARD_THRESHOLD_MAX_THREADS: int = CPU_COUNT * 4  # protect from overly big number of threads to use
PATH_LEN_MAX_LIMIT: int = 15  # limit path len to be practical in terms of latency and reliability of path
