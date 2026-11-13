import json
from fractions import Fraction
from pathlib import Path


def dot(left, right):
    return sum(first * second for first, second in zip(left, right))


def multiply(matrix, vector):
    return [dot(row, vector) for row in matrix]


def witness(dimension, count):
    coefficient_a = Fraction(2, 3)
    coefficient_b = Fraction(1, 4)
    coefficient_d = 1 - coefficient_a - coefficient_b
    signs = [1] * count + [-1] * (dimension - count)
    matrix = [
        [
            coefficient_d * (row == column)
            + coefficient_a * signs[row] * signs[column]
            + coefficient_b
            for column in range(dimension)
        ]
        for row in range(dimension)
    ]
    pairs = [matrix[row][column] for row in range(dimension) for column in range(row)]
    mean = sum(pairs) / len(pairs)
    variance = sum(entry * entry for entry in pairs) / len(pairs) - mean * mean
    sign_mean = Fraction((2 * count - dimension) ** 2 - dimension, dimension * (dimension - 1))
    assert mean == coefficient_a * sign_mean + coefficient_b
    assert variance == coefficient_a ** 2 * (1 - sign_mean ** 2)
    assert all(matrix[index][index] == 1 for index in range(dimension))
    assert 0 < mean < Fraction(1, 2)
    assert variance > mean ** 2
    assert mean ** 2 + variance < 1
    assert variance >= (1 - mean) ** 2
    assert variance <= 3 * mean ** 2
    trace = dimension * (coefficient_a + coefficient_b)
    rayleigh = coefficient_a * Fraction(sum(signs) ** 2, dimension) + coefficient_b * dimension
    determinant = coefficient_a * coefficient_b * (dimension ** 2 - sum(signs) ** 2)
    assert trace > 0 and determinant > 0 and trace ** 2 - 4 * determinant > 0
    assert 2 * rayleigh < trace
    assert 2 * (dimension - 1) * mean < (dimension - 2) * (coefficient_a + coefficient_b)
    ones = [1] * dimension
    matrix_ones = multiply(matrix, ones)
    assert dot(ones, matrix_ones) / dimension == 1 + (dimension - 1) * mean
    frobenius = sum(entry ** 2 for row in matrix for entry in row)
    assert frobenius == dimension + dimension * (dimension - 1) * (mean ** 2 + variance)
    result = {
        'dimension': dimension,
        'plus_signs': count,
        'mean': str(mean),
        'variance': str(variance),
        'scalar_diagonal': str(coefficient_d),
        'rank_two_trace': str(trace),
        'rank_two_determinant': str(determinant),
        'rank_two_rayleigh': str(rayleigh),
        'domain': 'D with sigma > c',
        'positive_definiteness': 'd I + a s s^T + b e e^T with a, b, d positive',
        'weight_gap': 'two positive simple spectral directions, with 2 r < T',
    }
    if dimension == 16:
        top = [1 + 4 * sign for sign in signs]
        second = [3 - 2 * sign for sign in signs]
        assert multiply(matrix, top) == [Fraction(145, 12) * entry for entry in top]
        assert multiply(matrix, second) == [Fraction(11, 4) * entry for entry in second]
        assert dot(top, second) == 0
        top_weight = Fraction(sum(top) ** 2, dimension * dot(top, top))
        second_weight = Fraction(sum(second) ** 2, dimension * dot(second, second))
        assert top_weight == Fraction(3, 7)
        assert second_weight == Fraction(4, 7)
        result['eigenvalues'] = ['145/12', '11/4', '1/12 (multiplicity 14)']
        result['positive_direction_weights'] = [str(top_weight), str(second_weight)]
    return result


def energy_controls():
    controls = 0
    equality_controls = 0
    for dimension in range(3, 31):
        equality_vector = [dimension - 2, dimension - 2] + [-2] * (dimension - 2)
        pair_sum = equality_vector[0] + equality_vector[1]
        assert dimension * pair_sum ** 2 == 2 * (dimension - 2) * dot(equality_vector, equality_vector)
        equality_controls += 1
        for seed in range(1, 26):
            vector = [((index + 1) * seed + index ** 2) % 17 - 8 for index in range(dimension - 1)]
            vector.append(-sum(vector))
            assert sum(vector) == 0
            for first, second in [(0, 1), (0, dimension - 1), (dimension - 2, dimension - 1)]:
                pair_sum = vector[first] + vector[second]
                assert dimension * pair_sum ** 2 <= 2 * (dimension - 2) * dot(vector, vector)
                controls += 1
    return {'dimensions': [3, 30], 'inequality_controls': controls, 'equality_controls': equality_controls}


def boundary_controls():
    zero_mean = []
    circle_count = 0
    negative_circle_count = 0
    for dimension in range(4, 41):
        count = (dimension + 1) // 2
        signs = [1] * count + [-1] * (dimension - count)
        sign_mean = Fraction(sum(signs) ** 2 - dimension, dimension * (dimension - 1))
        expected_mean = -Fraction(1, dimension - 1 if dimension % 2 == 0 else dimension)
        assert sign_mean == expected_mean
        coefficient_a = Fraction(3, 5)
        coefficient_b = -coefficient_a * sign_mean
        coefficient_d = 1 - coefficient_a - coefficient_b
        assert coefficient_a > coefficient_b > 0 and coefficient_d > 0
        matrix = [[coefficient_d * (row == column) + coefficient_a * signs[row] * signs[column] + coefficient_b
                   for column in range(dimension)] for row in range(dimension)]
        pairs = [matrix[row][column] for row in range(dimension) for column in range(row)]
        assert all(matrix[index][index] == 1 for index in range(dimension))
        assert sum(pairs) == 0
        variance = sum(entry * entry for entry in pairs) / len(pairs)
        assert variance == coefficient_a ** 2 * (1 - sign_mean ** 2)
        trace = dimension * (coefficient_a + coefficient_b)
        rayleigh = coefficient_a + coefficient_b
        determinant = coefficient_a * coefficient_b * (dimension ** 2 - sum(signs) ** 2)
        assert trace ** 2 - 4 * determinant > 0 and determinant > 0
        assert 2 * rayleigh < trace
        zero_mean.append({'dimension': dimension, 'variance': str(variance), 'mean': '0'})
        for plus_count in range(dimension + 1):
            top_mass = Fraction((2 * plus_count - dimension) ** 2, dimension ** 2)
            mean = Fraction((2 * plus_count - dimension) ** 2 - dimension, dimension * (dimension - 1))
            other_mean_mass = (1 - top_mass) / (dimension - 1)
            assert (top_mass < other_mean_mass) == (mean < 0)
            circle_count += 1
            negative_circle_count += mean < 0
    return {
        'dimensions': [4, 40],
        'zero_mean_witnesses': zero_mean,
        'circular_boundary_controls': circle_count,
        'negative_mean_circular_controls': negative_circle_count,
        'scope': 'Exact zero-mean rank-two witnesses and the rank-one eigenspace criterion; fixed-parameter eventual existence has a written proof in note.tex.',
    }


def main():
    result = {
        'schema_version': 1,
        'arithmetic': 'exact rational and integer',
        'coverage': 'Four positive-mean rank-two correlation matrices, zero-mean and circular-boundary controls, and finite centered-energy controls; quantified statements have written proofs in note.tex.',
        'witnesses': [witness(dimension, count) for dimension, count in [(16, 12), (17, 13), (24, 18), (100, 74)]],
        'centered_energy': energy_controls(),
        'boundary_controls': boundary_controls(),
        'status': 'all exact checks passed',
    }
    content = json.dumps(result, indent=2, sort_keys=True) + '\n'
    Path(__file__).with_name('checks.json').write_text(content)
    print(content, end='')


if __name__ == '__main__':
    main()
