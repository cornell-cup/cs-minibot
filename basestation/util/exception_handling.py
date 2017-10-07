import traceback


def log_exn_info(e, msg=""):
    """
    Logs the information of the error message in msg with a stack traceback

    Args:
        e (exn): The exception thrown. Its traceback will be logged
        msg (str): Message to log, default is "" (empty string)
    """
    print(msg)  # currently printing instead of logging
    print("\033[91m" + "[ ERROR ]: " + e.strerror + "\033[0m")
    traceback.print_tb(e.__traceback__)
    return
