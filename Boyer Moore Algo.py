def preprocess_bad_character(pattern):
    """Generate bad character table: maps character to its last index in the pattern."""
    return {char: i for i, char in enumerate(pattern)}  # For each character, store its last occurrence index


def preprocess_good_suffix(pattern):
    """Generate good suffix shift tables L and l."""
    m = len(pattern)
    N = [0] * m  # N[i]: length of the longest suffix ending at i that is also a prefix
    L = [0] * m  # L[i]: largest position less than m such that substring P[i:] matches a suffix of P[0:j]
    l = [0] * (m + 1)  # l[i]: length of the largest suffix of P[0:i] that is also a prefix of P

    # Compute N array (Z-array in reverse)
    N[m - 1] = m  # The whole pattern is a suffix of itself
    g = m - 1
    f = m - 1
    for i in range(m - 2, -1, -1):  # Loop from second last to first character
        if i > g and N[i + m - 1 - f] < i - g:
            N[i] = N[i + m - 1 - f]  # Use previously computed values to avoid rechecking
        else:
            g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1  # Compare backwards for longest suffix
            N[i] = f - g  # Store the matched suffix length

    # Compute L array from N
    for j in range(m - 1):
        i = m - N[j]
        if i < m:
            L[i] = j + 1  # Set the appropriate shift index based on N values

    # Compute l' array from N
    for i in range(m):
        if N[i] > 0:
            l[m - N[i]] = i  # Set shift for full match suffixes
    for i in range(m - 1, 0, -1):
        if l[i] == 0:
            l[i] = l[i + 1]  # Fill in 0s with next known suffix shift

    return L, l


def boyer_moore(text, pattern):
    """Search pattern in text using Boyer-Moore algorithm with debug prints."""
    if not pattern or not text or len(pattern) > len(text):
        return []  # Edge case: invalid input

    # Preprocessing phase
    bad_char = preprocess_bad_character(pattern)
    L, l = preprocess_good_suffix(pattern)

    m = len(pattern)
    n = len(text)
    positions = []  # Store matched positions
    s = 0  # Shift of the pattern with respect to text

    while s <= n - m:
        j = m - 1  # Start comparing from the end of the pattern
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1  # Keep moving left if characters match

        # Debug print current alignment
        print("\nText    :", text)
        print("Pattern :", ' ' * s + pattern)

        if j < 0:
            # Match found
            print(f"Match found at index {s}. Shifting pattern by {m - l[1] if m > 1 else 1} (Good Suffix Rule).")
            positions.append(s)
            s += m - l[1] if m > 1 else 1  # Shift pattern by full match rule
        else:
            # Mismatch occurred
            bad_char_shift = j - bad_char.get(text[s + j], -1)  # Shift based on last occurrence of bad character

            # Compute good suffix shift
            if j + 1 == m:
                good_suffix_shift = 1  # No suffix exists
            elif L[j + 1] > 0:
                good_suffix_shift = m - L[j + 1]
            else:
                good_suffix_shift = m - l[j + 1]

            # Choose the maximum shift between bad character and good suffix rule
            final_shift = max(bad_char_shift, good_suffix_shift)
            rule = "Bad Character" if bad_char_shift >= good_suffix_shift else "Good Suffix"

            print(f"Mismatch at pattern[{j}] and text[{s + j}] "
                  f"(text char: '{text[s + j]}', pattern char: '{pattern[j]}')")
            print(f"Shifting by {final_shift} using {rule} Rule.")
            s += final_shift  # Shift the pattern

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
