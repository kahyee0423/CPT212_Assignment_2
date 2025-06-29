NO_OF_CHARS = 256  # Standard ASCII table size

def bad_char_heuristic(pattern):
    """
    Preprocess the pattern to create the bad character table.
    Each character maps to its last index in the pattern.
    """
    bad_char = [-1] * NO_OF_CHARS
    for i in range(len(pattern)):
        bad_char[ord(pattern[i])] = i
    return bad_char

def good_suffix_heuristic(pattern):
    """
    Preprocess the pattern to create the good suffix shift tables (L and l).
    These are used to determine the shift amount when a suffix match occurs.
    """
    m = len(pattern)
    N = [0] * m
    L = [0] * m
    l = [0] * (m + 1)

    # Compute N array using a reversed Z-algorithm
    N[m - 1] = m
    g = m - 1
    f = m - 1
    for i in range(m - 2, -1, -1):
        if i > g and N[i + m - 1 - f] < i - g:
            N[i] = N[i + m - 1 - f]
        else:
            g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            N[i] = f - g

    # Compute L table from N
    for j in range(m - 1):
        i = m - N[j]
        if i < m:
            L[i] = j + 1

    # Compute l table from N
    for i in range(m):
        if N[i] > 0:
            l[m - N[i]] = i
    for i in range(m - 1, 0, -1):
        if l[i] == 0:
            l[i] = l[i + 1]

    return L, l

def boyer_moore(text, pattern):
    """
    Performs Boyer-Moore search on the input text using both
    Bad Character and Good Suffix heuristics.
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n < m:
        return []

    # Preprocess pattern
    bad_char = bad_char_heuristic(pattern)
    L, l = good_suffix_heuristic(pattern)

    positions = []
    s = 0  # shift of pattern relative to text

    while s <= n - m:
        j = m - 1

        # Compare pattern with text from right to left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # Debug visual output
        print("\nText    :", text)
        print("Pattern :", " " * s + pattern)

        if j < 0:
            # Match found
            positions.append(s)
            # Shift by the period of the pattern (m - l[1])
            shift = m - l[1] if m > 1 else 1
            print(f"Match found at index {s}. Shifting by {shift} using Good Suffix rule.")
            s += shift
        else:
            # Mismatch: calculate shifts
            mismatched_char = text[s + j]
            bc_ord = ord(mismatched_char)

            # Bad Character Shift
            if bc_ord < NO_OF_CHARS and bad_char[bc_ord] != -1:
                bc_shift = max(1, j - bad_char[bc_ord])
            else:
                bc_shift = j + 1  # Character not found in pattern

            # Good Suffix Shift
            if j == m - 1:
                gs_shift = 1  # No good suffix exists
            elif L[j + 1] > 0:
                gs_shift = m - L[j + 1]  # Case 1: Strong good suffix
            else:
                gs_shift = m - l[j + 1]  # Case 2: Prefix matching

            shift = max(bc_shift, gs_shift)
            rule_used = "Bad Character" if bc_shift >= gs_shift else "Good Suffix"
            
            print(f"Mismatch at index {s + j} (text char: '{mismatched_char}', pattern char: '{pattern[j]}').")
            print(f"Bad Character shift: {bc_shift}, Good Suffix shift: {gs_shift}")
            print(f"Shifting by {shift} position using {rule_used} rule.")
            
            s += shift

    return positions

def main():
    # User input for text and pattern
    text = input("Enter the text: ")
    pattern = input("Enter the pattern to find: ")

    matches = boyer_moore(text, pattern)

    if matches:
        print("\nPattern found at positions:", matches)
    else:
        print("\nPattern not found.")


if __name__ == "__main__":
    main()
