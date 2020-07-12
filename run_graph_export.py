"""
This program creates an inverse Collatz graph, consisting of odd numbers and exports
the results to csv.
"""

# Imports
import logging
from collatz import graph


def _main():
    """
    This method executes the program.
    :return: None.
    """
    # Configuration
    file_name = "data/collatz_graph.csv"
    iterations = 3
    k_factor = 5
    predecessor_count = 5

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    # Create graph
    logging.info("Creating Collatz inverse graph...")

    result_frame = graph.create_collatz_graph(
        1, k=k_factor, predecessor_count=predecessor_count, iteration_count=iterations)

    result_frame[["successor", "predecessor"]].to_csv(file_name, index=False, header=False)

    logging.info("Export finished successfully!")


# Main method to start the program
if __name__ == '__main__':
    _main()
