"""
Everything below here is for testing. The values in 'values' are precomputed from
the smolyak sparse grid matlab code. They should match our c++ version or something
is wrong.
"""
from puq.sparse_grid import sgrid
from numpy import array, asarray, zeros

values = \
[
    array([[ -1.00000000000000000e+00, 3.3333333333333315e-01],
        [ -6.12323399573676604e-17, 1.33333333333333326e+00],
        [  1.00000000000000000e+00, 3.33333333333333315e-01]]),
    array([[ -1.00000000000000000e+00, 6.66666666666666657e-02],
        [ -7.07106781186547573e-01, 5.33333333333333326e-01],
        [ -6.12323399573676604e-17, 8.00000000000000044e-01],
        [  7.07106781186547462e-01, 5.33333333333333437e-01],
        [  1.00000000000000000e+00, 6.66666666666666657e-02]]),
    array([[ -1.00000000000000000e+00, 1.58730158730158721e-02],
        [ -9.23879532511286738e-01, 1.46218649216018126e-01],
        [ -7.07106781186547573e-01, 2.79365079365079372e-01],
        [ -3.82683432365089837e-01, 3.61717858720489727e-01],
        [ -6.12323399573676604e-17, 3.93650793650793640e-01],
        [  3.82683432365089726e-01, 3.61717858720489782e-01],
        [  7.07106781186547462e-01, 2.79365079365079427e-01],
        [  9.23879532511286738e-01, 1.46218649216018182e-01],
        [  1.00000000000000000e+00, 1.58730158730158721e-02]]),
    array([[ -1.00000000000000000e+00, 3.92156862745098034e-03],
        [ -9.80785280403230431e-01, 3.73687028372056002e-02],
        [ -9.23879532511286738e-01, 7.54823315431518288e-02],
        [ -8.31469612302545236e-01, 1.08905552581890941e-01],
        [ -7.07106781186547573e-01, 1.38956468368233083e-01],
        [ -5.55570233019602289e-01, 1.63172664281703322e-01],
        [ -3.82683432365089837e-01, 1.81473784236493352e-01],
        [ -1.95090322016128331e-01, 1.92513864612925689e-01],
        [ -6.12323399573676604e-17, 1.96410125821890491e-01],
        [  1.95090322016128193e-01, 1.92513864612925661e-01],
        [  3.82683432365089726e-01, 1.81473784236493352e-01],
        [  5.55570233019601956e-01, 1.63172664281703350e-01],
        [  7.07106781186547462e-01, 1.38956468368233083e-01],
        [  8.31469612302545347e-01, 1.08905552581890913e-01],
        [  9.23879532511286738e-01, 7.54823315431518427e-02],
        [  9.80785280403230431e-01, 3.73687028372056695e-02],
        [  1.00000000000000000e+00, 3.92156862745098034e-03]]),
    array([[ -1.00000000000000000e+00, 0.00000000000000000e+00, 6.66666666666666630e-01],
        [ -6.12323399573676604e-17, 0.00000000000000000e+00, 1.33333333333333304e+00],
        [  1.00000000000000000e+00, 0.00000000000000000e+00, 6.6666666666666630e-01],
        [  0.00000000000000000e+00, -1.00000000000000000e+00,6.66666666666666630e-01],
        [  0.00000000000000000e+00, 1.00000000000000000e+00, 6.66666666666666630e-01]]),
    array([[ -1.00000000000000000e+00, 0.00000000000000000e+00, -1.90476190476190466e-01],
        [ -9.23879532511286738e-01, 0.00000000000000000e+00, 2.92437298432036252e-01],
        [ -7.07106781186547573e-01, 0.00000000000000000e+00, 2.03174603174603119e-01],
        [ -3.82683432365089837e-01, 0.00000000000000000e+00, 7.23435717440979453e-01],
        [ -6.12323399573676604e-17, 0.00000000000000000e+00, -1.26984126984126977e+00],
        [  3.82683432365089726e-01, 0.00000000000000000e+00, 7.23435717440979564e-01],
        [  7.07106781186547462e-01, 0.00000000000000000e+00, 2.03174603174603341e-01],
        [  9.23879532511286738e-01, 0.00000000000000000e+00, 2.92437298432036363e-01],
        [  1.00000000000000000e+00, 0.00000000000000000e+00, -1.90476190476190466e-01],
        [ -1.00000000000000000e+00, -1.00000000000000000e+00, -6.66666666666666657e-02],
        [ -1.00000000000000000e+00, 1.00000000000000000e+00, -6.66666666666666657e-02],
        [ -7.07106781186547573e-01, -1.00000000000000000e+00, 1.77777777777777757e-01],
        [ -7.07106781186547573e-01, 1.00000000000000000e+00, 1.77777777777777757e-01],
        [ -6.12323399573676604e-17, -1.00000000000000000e+00, -1.90476190476190466e-01],
        [ -6.12323399573676604e-17, 1.00000000000000000e+00, -1.90476190476190466e-01],
        [  7.07106781186547462e-01, -1.00000000000000000e+00, 1.77777777777777812e-01],
        [  7.07106781186547462e-01, 1.00000000000000000e+00, 1.77777777777777812e-01],
        [  1.00000000000000000e+00, -1.00000000000000000e+00, -6.66666666666666657e-02],
        [  1.00000000000000000e+00, 1.00000000000000000e+00, -6.66666666666666657e-02],
        [ -1.00000000000000000e+00, -7.07106781186547573e-01, 1.77777777777777757e-01],
        [ -1.00000000000000000e+00, 7.07106781186547462e-01, 1.77777777777777812e-01],
        [ -6.12323399573676604e-17, -7.07106781186547573e-01, 2.03174603174603119e-01],
        [ -6.12323399573676604e-17, 7.07106781186547462e-01, 2.03174603174603341e-01],
        [  1.00000000000000000e+00, -7.07106781186547573e-01, 1.77777777777777757e-01],
        [  1.00000000000000000e+00, 7.07106781186547462e-01, 1.77777777777777812e-01],
        [  0.00000000000000000e+00, -9.23879532511286738e-01, 2.92437298432036252e-01],
        [  0.00000000000000000e+00, -3.82683432365089837e-01, 7.23435717440979453e-01],
        [  0.00000000000000000e+00, 3.82683432365089726e-01, 7.23435717440979564e-01],
        [  0.00000000000000000e+00, 9.23879532511286738e-01, 2.92437298432036363e-01]]),
    array([[ -1.00000000000000000e+00, 0.00000000000000000e+00,
                0.00000000000000000e+00, -6.22222222222222232e-01],
             [ -7.07106781186547573e-01, 0.00000000000000000e+00,
                0.00000000000000000e+00, 2.13333333333333330e+00],
             [ -6.12323399573676604e-17, 0.00000000000000000e+00,
                0.00000000000000000e+00, -3.73333333333333783e+00],
             [  7.07106781186547462e-01, 0.00000000000000000e+00,
                0.00000000000000000e+00, 2.13333333333333375e+00],
             [  1.00000000000000000e+00, 0.00000000000000000e+00,
                0.00000000000000000e+00, -6.22222222222222232e-01],
             [ -1.00000000000000000e+00, -1.00000000000000000e+00,
                0.00000000000000000e+00, 2.22222222222222210e-01],
             [ -1.00000000000000000e+00, 1.00000000000000000e+00,
                0.00000000000000000e+00, 2.22222222222222210e-01],
             [ -6.12323399573676604e-17, -1.00000000000000000e+00,
                0.00000000000000000e+00, -6.22222222222222232e-01],
             [ -6.12323399573676604e-17, 1.00000000000000000e+00,
                0.00000000000000000e+00, -6.22222222222222232e-01],
             [  1.00000000000000000e+00, -1.00000000000000000e+00,
                0.00000000000000000e+00, 2.22222222222222210e-01],
             [  1.00000000000000000e+00, 1.00000000000000000e+00,
                0.00000000000000000e+00, 2.22222222222222210e-01],
             [ -1.00000000000000000e+00, 0.00000000000000000e+00,
                - 1.00000000000000000e+00, 2.22222222222222210e-01],
             [ -1.00000000000000000e+00, 0.00000000000000000e+00,
                1.00000000000000000e+00, 2.22222222222222210e-01],
             [ -6.12323399573676604e-17, 0.00000000000000000e+00,
                - 1.00000000000000000e+00, -6.22222222222222232e-01],
             [ -6.12323399573676604e-17, 0.00000000000000000e+00,
                1.00000000000000000e+00, -6.22222222222222232e-01],
             [  1.00000000000000000e+00, 0.00000000000000000e+00,
                - 1.00000000000000000e+00, 2.22222222222222210e-01],
             [  1.00000000000000000e+00, 0.00000000000000000e+00,
                1.00000000000000000e+00, 2.22222222222222210e-01],
             [  0.00000000000000000e+00, -7.07106781186547573e-01,
                0.00000000000000000e+00, 2.13333333333333330e+00],
             [  0.00000000000000000e+00, 7.07106781186547462e-01,
                0.00000000000000000e+00, 2.13333333333333375e+00],
             [  0.00000000000000000e+00, -1.00000000000000000e+00,
                - 1.00000000000000000e+00, 2.22222222222222210e-01],
             [  0.00000000000000000e+00, -1.00000000000000000e+00,
                1.00000000000000000e+00, 2.22222222222222210e-01],
             [  0.00000000000000000e+00, 1.00000000000000000e+00,
                - 1.00000000000000000e+00, 2.22222222222222210e-01],
             [  0.00000000000000000e+00, 1.00000000000000000e+00,
                1.00000000000000000e+00, 2.22222222222222210e-01],
             [  0.00000000000000000e+00, 0.00000000000000000e+00,
                - 7.07106781186547573e-01, 2.13333333333333330e+00],
             [  0.00000000000000000e+00, 0.00000000000000000e+00,
                7.07106781186547462e-01, 2.13333333333333375e+00]]),
]

# return 0 if two numbers are equal
def compare_nums(a, b):
    if a == b:
        return 0
    try:
        fa = float(a)
        fb = float(b)
        if abs(fa - fb) <= 1.0e-9:
            return 0
    except:
        pass
    return 1

def compare_vectors(vec1, vec2):
    for a, b in zip(vec1, vec2):
        if compare_nums(a, b):
            return 1
    return 0

def find_match(x, a):
    row = 0
    for c in a:
        if compare_vectors(x, c) == 0:
            return row
        row += 1

    assert False

def _sscc_tst(d, l):
    return sgrid(d,l)

def test_sscc_1_1():
    expected = values[0]
    do_tst(1,1,expected)
def test_sscc_1_2():
    expected = values[1]
    do_tst(1,2,expected)
def test_sscc_1_3():
    expected = values[2]
    do_tst(1,3,expected)
def test_sscc_1_4():
    expected = values[3]
    do_tst(1,4,expected)
def test_sscc_2_1():
    expected = values[4]
    do_tst(2,1,expected)
def test_sscc_2_3():
    expected = values[5]
    do_tst(2,3,expected)
def test_sscc_3_2():
    expected = values[6]
    do_tst(3,2,expected)

def do_tst(d, l, res):
    tmp = _sscc_tst(d, l)
    z = zeros(len(tmp))
    i = 0
    for x in tmp:
        n = find_match(x, res)
        z[n] = 1
        i += 1
    assert z.all()

