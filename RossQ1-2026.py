from typing import List, Tuple, Set
import sys


def circle_distance(i, j, total):
    # Finds the shortest path around the circle between two dots
    diff = abs(i - j) % total
    return min(diff, total - diff)


def normalize_matching(pairs, total):
    # Creates one standard version of a pattern so the same arrangement is not counted twice
    n = total // 2
    canonical = None
    # Try every possible turn and flip of the circle
    for rot in range(total):
        for reflect in [False, True]:
            transformed = []
            for a, b in pairs:
                aa = (a + rot) % total
                bb = (b + rot) % total
                if reflect:
                    aa = (-aa) % total
                    bb = (-bb) % total
                transformed.append(tuple(sorted([aa, bb])))
            transformed.sort()
            transformed_tuple = tuple(transformed)
            if canonical is None or transformed_tuple < canonical:
                canonical = transformed_tuple
    return canonical


def find_all_tsuro_cards(n):
    # Looks for every possible way to connect all dots using each length once
    if n < 1:
        return []
    total = 2 * n
    solutions = []
    def backtrack(paired, used_weights, current_pairs, start_node):
        # When every dot is connected, save the result
        if len(current_pairs) == n:
            solution = sorted(current_pairs)
            solutions.append(solution)
            return
        # Find the lowest numbered dot that is still free
        i = -1
        for node in range(start_node, total):
            if not paired[node]:
                i = node
                break
        if i == -1:
            return
        # Try each possible length from shortest to longest
        for k in range(1, n + 1):
            if k in used_weights:
                continue
            # Check both directions around the circle
            for direction in [1, -1]:
                j = (i + direction * k) % total
                if j == i or paired[j]:
                    continue
                w = circle_distance(i, j, total)
                if w != k:
                    continue
                pair = tuple(sorted([i, j]))
                # Connect the dots and continue
                paired[i] = paired[j] = True
                used_weights.add(k)
                current_pairs.append(pair)
                next_start = 0 if all(paired[:i+1]) else i + 1
                backtrack(paired, used_weights, current_pairs, next_start)
                # Undo the connection and try the next option
                current_pairs.pop()
                used_weights.remove(k)
                paired[i] = paired[j] = False
    paired = [False] * total
    backtrack(paired, set(), [], 0)
    # Remove the extra copies so each drawing appears only once
    seen = set()
    clean = []
    for sol in solutions:
        fs = frozenset(sol)
        if fs not in seen:
            seen.add(fs)
            clean.append(sol)
    return clean
    return solutions


def find_unique_tsuro_cards(n):
    # Takes the full list and keeps only the different patterns (same shape counts as one)
    all_solutions = find_all_tsuro_cards(n)
    if not all_solutions:
        return []
    seen = set()
    unique = []
    for sol in all_solutions:
        canon = normalize_matching(sol, 2 * n)
        if canon not in seen:
            seen.add(canon)
            unique.append([list(p) for p in canon])
    unique.sort(key=lambda x: tuple(tuple(p) for p in x))
    return unique


def print_solutions(n, solutions, label="solutions"):
    # Shows the results in a clear list
    count = len(solutions)
    print(f"\nFor n = {n}: found {count} {label}\n")
    if count == 0:
        print("None exist.\n")
        return
    for idx, sol in enumerate(solutions, 1):
        print(f"{label.capitalize()} #{idx}:")
        for a, b in sol:
            dist = circle_distance(a, b, 2 * n)
            print(f"  {a:2d} — {b:2d}  (weight {dist})")
        print()


# Example usage — change the numbers to try different sizes
if __name__ == "__main__":
    for n_val in [4, 5]:
        print(f"\n{'='*50}\nn = {n_val}\n{'='*50}")
        all_sols = find_all_tsuro_cards(n_val)
        print_solutions(n_val, all_sols, "labeled tsuro n-card")
        unique_sols = find_unique_tsuro_cards(n_val)
        print_solutions(n_val, unique_sols, "structurally distinct (up to dihedral symmetry)")