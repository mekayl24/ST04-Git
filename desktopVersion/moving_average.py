def moving_average(data, window_size):
    """
    Compute the moving average of a list of data.

    Parameters:
        data (list): The input data.
        window_size (int): The size of the moving average window.

    Returns:
        list: The smoothed data.
    """
    moving_averages = []
    for i in range(len(data)):
        window = data[max(0, i - window_size + 1):i + 1]
        moving_averages.append(sum(window) / len(window))
    return moving_averages