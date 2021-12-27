from typing import Tuple


def search_filter(candidate: str, search_words: str) -> Tuple[bool, int]:
    next_candidate = candidate
    if search_words.lower() == candidate.lower():
        rank = 0  # Matches completely
        return True, rank
    elif search_words.lower() in candidate[:len(search_words)].lower():
        rank = 1  # Matches so far
        return True, rank
    elif search_words.lower() in candidate.lower():
        rank = 2  # Contains
        return True, rank

    rank = 0
    for n, element in enumerate(search_words):
        try:
            index_ = next_candidate.lower().index(element.lower())
        except ValueError:
            return False, rank  # rank does not matter for False / eliminated candidates
        next_candidate = next_candidate[index_:]

    rank = 3
    return True, rank


if __name__ == '__main__':
    candidates = (
        'Tr_Revenue',
        'Tr_COGS',
        'Targets',
    )

    search_words_ = 'tg'
    expectation = (
        'Tr_COGS',
        'Targets',
    )

    results = [candidate for candidate in candidates if search_filter(candidate, search_words_)[0]]
    print(tuple(expectation))
    print(tuple(results))
    print(tuple(expectation) == tuple(results))
