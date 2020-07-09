"""
This program creates an inverse Collatz graph, consisting of odd numbers and exports
the results to csv.
"""

# Imports
import logging
from collatz import graph

# Configuration
FILE_NAME = "data/collatz_graph.csv"
ITERATIONS = 3
K_FACTOR = 5
PREDECESSOR_COUNT = 5
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Create graph
logging.info("Creating Collatz inverse graph...")

RESULT_FRAME = graph.create_collatz_graph(
    1, k=K_FACTOR, predecessor_count=PREDECESSOR_COUNT, iteration_count=ITERATIONS)

RESULT_FRAME[["successor", "predecessor"]].to_csv(FILE_NAME, index=False, header=False)

logging.info("Export finished successfully!")
