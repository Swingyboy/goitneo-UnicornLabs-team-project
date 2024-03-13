from typing import Any, List, Optional, Tuple
import re


def _find_best_match(input_value: str, str_list: List[str]) -> Optional[str]:
    """Find the best match for the input_value in the list of strings."""
    best_match: Optional[Any] = None
    best_score: int = 0  # Initialize to 0 for matching pattern

    pattern = re.compile(input_value)

    for s in str_list:
        match = pattern.search(s)
        if match and match.end() - match.start() > best_score:
            best_score = match.end() - match.start()
            best_match = s

    return best_match


def _parse_input(user_input: str) -> Tuple[str, ...]:
    """Parse the user input and return the command and its arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
