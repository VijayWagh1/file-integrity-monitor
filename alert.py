def alert(message):
    """
    Alert function to notify about detected anomalies.
    Currently prints to console. Can be extended to send emails or other notifications.
    """
    print(f"ALERT: {message}")
    # TODO: Implement email alerts if configured in config.ini