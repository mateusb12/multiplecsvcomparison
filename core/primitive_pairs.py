def generate_primitive_pairs(min_value: int = 0, max_value: int = 100, difference: int = 25, step: int = 5) -> list:
    pairs = []
    # Generate pairs such that x + difference <= max_value
    for x in range(min_value, max_value - difference + 1, step):
        y = x + difference
        pairs.append((x, y))
    return pairs


def main():
    primitive = generate_primitive_pairs()
    print(primitive)


if __name__ == "__main__":
    main()
