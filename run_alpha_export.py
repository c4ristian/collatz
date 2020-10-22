"""
This program exports data on the alphas of Collatz sequences and related features
into a csv file. Only odd Collatz numbers are included. The sample is used
to validate mathematical theorems and for the training of machine learning
models.
"""
import shutil
import logging
from math import log2
import pandas as pd
from collatz import commons


def _generate_odd_sequence(sequence_id: int, start_value: int,
                           k_factor: int, max_iterations: int):
    """
    This method generates a Collatz sequence containing only odd numbers.

    :param sequence_id: ID of the sequence.
    :param start_value: The integer value to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k_factor: The factor by which odd numbers are multiplied in the sequence.
    :param max_iterations: The maximum number of iterations performed
        before the method exits.
    :return: The Collatz sequence as a pandas data frame.
    """
    odds = commons.odd_collatz_sequence(start_value, k_factor, max_iterations)
    next_odds = odds[1:]
    odds.pop()

    collatz_frame = pd.DataFrame({"v_i": odds})
    collatz_frame["sequence_id"] = sequence_id
    collatz_frame["sequence_len"] = len(collatz_frame)
    collatz_frame["n"] = collatz_frame.index + 1
    collatz_frame["k_factor"] = k_factor

    collatz_frame["v_1"] = start_value
    collatz_frame["kv_i+1"] = collatz_frame["v_i"].apply(
        commons.next_collatz_number, args=(k_factor,))
    collatz_frame["v_i+"] = next_odds

    collatz_frame["terminal"] = collatz_frame["v_i+"] == 1
    collatz_frame["cycle"] = collatz_frame["v_i+"] == collatz_frame["v_1"]

    # Logs
    collatz_frame["v_i_log2"] = collatz_frame["v_i"].apply(log2)
    collatz_frame["kv_i+1_log2"] = collatz_frame["kv_i+1"].apply(log2)
    collatz_frame["v_i+_log2"] = collatz_frame["v_i+"].apply(log2)

    # Binary strings
    collatz_frame["v_1_bin"] = collatz_frame["v_1"].apply(commons.to_binary)
    collatz_frame["v_i_bin"] = collatz_frame["v_i"].apply(commons.to_binary)

    # Mods
    collatz_frame["v_i_mod4"] = collatz_frame["v_i"] % 4
    collatz_frame["kv_i+1_mod4"] = collatz_frame["kv_i+1"] % 4
    collatz_frame["v_i+_mod4"] = collatz_frame["v_i+"] % 4

    # Alpha
    collatz_frame["alpha_i"] = collatz_frame["kv_i+1"].apply(commons.trailing_zeros)
    collatz_frame["alpha_i"] = collatz_frame["alpha_i"].astype('int64')
    collatz_frame["alpha_i_max"] = log2(k_factor) + collatz_frame["v_i"].apply(log2)
    collatz_frame["alpha_i_max"] += (1 + 1 / (k_factor * collatz_frame["v_i"])).apply(log2)
    # Round result here to avoid loss of precision errors
    collatz_frame["alpha_i_max"] = collatz_frame["alpha_i_max"].round(9)
    collatz_frame["alpha"] = collatz_frame["alpha_i"].cumsum()
    collatz_frame["alpha_cycle"] = (log2(k_factor) * collatz_frame["n"]).astype('int64') + 1
    collatz_frame["alpha_max"] = log2(start_value) + (collatz_frame["n"] * log2(k_factor))
    collatz_frame["alpha_max"] = collatz_frame["alpha_max"].astype('int64') + 1

    # Beta
    collatz_frame["beta_i"] = 1 + 1 / (k_factor * collatz_frame["v_i"])
    collatz_frame["beta"] = collatz_frame["beta_i"].cumprod()

    # Lambda
    collatz_frame["bin_len"] = collatz_frame["v_i_log2"].astype('int64') + 1
    collatz_frame["next_bin_len"] = collatz_frame["kv_i+1_log2"].astype('int64') + 1

    collatz_frame["bin_diff"] = collatz_frame["next_bin_len"] - collatz_frame["bin_len"]
    collatz_frame["lambda_i"] = collatz_frame["bin_diff"]
    collatz_frame.loc[collatz_frame["lambda_i"] < 0, "lambda_i"] = 0
    collatz_frame["lambda"] = collatz_frame["lambda_i"].cumsum()

    collatz_frame["lambda_i_min"] = int(log2(k_factor))
    collatz_frame["lambda_i_max"] = int(log2(k_factor) + 1)

    collatz_frame["lambda_hyp"] = (collatz_frame["n"] * log2(k_factor))
    collatz_frame["lambda_min"] = collatz_frame["lambda_hyp"].astype('int64')
    collatz_frame["lambda_max"] = collatz_frame["lambda_hyp"].astype('int64') + 2

    # Omega
    collatz_frame["omega_i"] = collatz_frame["lambda_i"] - collatz_frame["alpha_i"]
    collatz_frame["omega"] = collatz_frame["lambda"] - collatz_frame["alpha"]

    collatz_frame["omega_i_max"] = collatz_frame["lambda_i_max"] - 1
    collatz_frame["omega_max"] = collatz_frame["lambda_max"] - collatz_frame["n"]

    result_frame = collatz_frame[[
        "sequence_id", "sequence_len", "n", "k_factor", "v_1",
        "v_i", "kv_i+1", "v_i+", "v_i_log2", "v_i+_log2", "kv_i+1_log2",
        "v_i_mod4", "kv_i+1_mod4", "v_i+_mod4",
        "v_1_bin", "v_i_bin", "terminal", "cycle",
        "alpha_i", "alpha_i_max", "alpha", "alpha_cycle", "alpha_max",
        "beta_i", "beta", "bin_len", "next_bin_len",
        "lambda_i", "lambda_i_min", "lambda_i_max",
        "lambda", "lambda_min", "lambda_max",
        "omega_i", "omega_i_max", "omega", "omega_max"]]

    result_frame.columns = [
        "sequence_id", "sequence_len", "n", "k", "v_1",
        "v_i", "kv_i+1", "v_i+", "v_i_log2", "v_i+_log2", "kv_i+1_log2",
        "v_i_mod4", "kv_i+1_mod4", "v_i+_mod4",
        "v_1_bin", "v_i_bin", "terminal", "cycle",
        "a_i", "a_i_max", "a", "a_cycle", "a_max",
        "b_i", "b", "bin_len", "next_bin_len",
        "l_i", "l_i_min", "l_i_max",
        "l", "l_min", "l_max",
        "o_i", "o_i_max", "o", "o_max"]

    return result_frame


def _main():
    """
    This method executes the program.
    :return: None.
    """
    k_factors = [1, 3, 5, 7, 9]
    max_start_value = 3999
    v_1_range = range(1, max_start_value + 1, 2)
    max_iterations = 100
    sequence_count = ((max_start_value + 1) / 2) * len(k_factors)

    export_name = "alpha_export"
    dest_file_name = "./data/" + export_name + ".csv"
    tmp_file_name = "./data/" + export_name + "_tmp" + ".csv"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Exporting %d Collatz sequences to file %s", sequence_count, dest_file_name)

    sequence_id = 0
    write_mode = True

    for k in k_factors:
        logging.info("Generating sequences for k=%d", k)

        for v_1 in v_1_range:
            # Create the sequence
            sequence_id = sequence_id + 1
            current_frame = _generate_odd_sequence(
                sequence_id, v_1, k, max_iterations)

            # Write the frame to file
            mode_flag = "w" if write_mode else "a"
            current_frame.to_csv(
                tmp_file_name, mode=mode_flag, index=False, header=write_mode)
            write_mode = False

    # Moving tmp file to destination file
    logging.info("Moving temp file to destination file")
    shutil.move(tmp_file_name, dest_file_name)

    # Export finished
    logging.info("Export finished successfully!")


# Main method to start the export
if __name__ == '__main__':
    _main()
