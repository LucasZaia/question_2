from langchain.tools import tool


@tool
def count_words(text: str) -> str:
    """Count the words in a text and return the total as a string."""
    return str(len(text.split()))

