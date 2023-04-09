import re
import logging


def format_title(title):
    # Remove any leading/trailing whitespace
    title = title.strip()

    # Remove text inside square brackets, parentheses, and curly braces
    title = re.sub(r"\[[^\]]*\]", "", title)
    title = re.sub(r"\([^\)]*\)", "", title)
    title = re.sub(r"\{[^\}]*\}", "", title)

    # If title doesn't end with a period, add one
    if title.endswith("."):
        title = title[:-1]

    # If title ends with a question mark or exclamation mark, remove it
    if title.endswith("?") or title.endswith("!"):
        title = title[:-1]

    # Capitalize the first letter of the title
    title = title[0].upper() + title[1:]

    # Replace multiple spaces with a single space
    title = " ".join(title.split())

    # If title is longer than 200 characters, truncate it and add "..." at the end
    if len(title) > 200:
        title = title[:200] + "..."

    return title


def get_logger(name):
    # Create a new logger with the specified name
    logger = logging.getLogger(name)

    # Set the logging level to DEBUG, so that all messages will be logged
    logger.setLevel(logging.DEBUG)

    # Create a formatter that specifies the format of the log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a new stream handler that will output the log messages to the console
    stream_handler = logging.StreamHandler()

    # Set the formatter of the stream handler to the formatter we created earlier
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

    # Return the logger
    return logger
