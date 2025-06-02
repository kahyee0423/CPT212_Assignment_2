def preprocess_bad_character(pattern):
    """Generate bad character table: maps character to its last index in the pattern."""
    return {char: i for i, char in enumerate(pattern)}

def preprocess_good_suffix(pattern):
    """Generate good suffix shift table L and l."""
    m = len(pattern)
    N = [0] * m
    L = [0] * m
    l = [0] * (m + 1)

    # Compute N array
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

    # Compute L array
    for j in range(m - 1):
        i = m - N[j]
        if i < m:
            L[i] = j + 1

    # Compute l' array
    for i in range(m):
        l[m - N[i]] = i

    return L, l

def boyer_moore(text, pattern):
    """Search pattern in text using Boyer-Moore algorithm with debug prints."""
    if not pattern or not text:
        return []

    bad_char = preprocess_bad_character(pattern)
    L, l = preprocess_good_suffix(pattern)

    m = len(pattern)
    n = len(text)
    positions = []
    s = 0  # shift

    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # Debug print current alignment
        print("\nText    :", text)
        print("Pattern :", ' ' * s + pattern)

        if j < 0:
            print(f"Match found at index {s}. Shifting pattern by {m - l[1] if m > 1 else 1} (Good Suffix Rule).")
            positions.append(s)
            s += m - l[1] if m > 1 else 1
        else:
            bad_char_shift = j - bad_char.get(text[s + j], -1)

            if j + 1 == m:
                good_suffix_shift = 1
            elif L[j + 1] > 0:
                good_suffix_shift = m - L[j + 1]
            else:
                good_suffix_shift = m - l[j + 1]

            final_shift = max(bad_char_shift, good_suffix_shift)
            rule = "Bad Character" if bad_char_shift >= good_suffix_shift else "Good Suffix"

            print(f"Mismatch at pattern[{j}] and text[{s + j}] (text char: '{text[s + j]}', pattern char: '{pattern[j]}')")
            print(f"Shifting by {final_shift} using {rule} Rule.")
            s += final_shift

    return positions

# Example usage
if __name__ == "__main__":
    text = input("Enter the text: ")
    pattern = input("Enter the pattern to find: ")

    matches = boyer_moore(text, pattern)

    if matches:
        print("\nPattern found at positions:", matches)
    else:
        print("\nPattern not found in the text.")