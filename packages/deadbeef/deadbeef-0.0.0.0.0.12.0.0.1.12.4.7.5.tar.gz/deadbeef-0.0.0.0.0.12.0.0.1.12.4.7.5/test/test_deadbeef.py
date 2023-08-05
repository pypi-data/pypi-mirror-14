import deadbeef

def test_count():
    assert deadbeef.candidate_count() > 4000

def test_string():
    n = deadbeef.get_string(10)
    assert len(n) == 10
    n_int = int(n, 16)
    assert hex(n_int)[2:] == n # nop

    m = deadbeef.get_string(8)
    assert len(m) == 8

    o = deadbeef.get_string(10)
    assert o != n

def test_int():
    n = deadbeef.get_int(10)
    assert len(hex(n)) == 12 # (including the '0x')

def test_filters():
    n = deadbeef.get_string(8, prefilter=lambda w: w.startswith('cool'))
    assert n.startswith('c001')

    n = deadbeef.get_string(postfilter=lambda w: len(w) > 2 and int(w, 16) % (16*16) == 6)
    assert n.endswith('06')

def test_skip():
    # just test if it doesn't except out for now
    deadbeef.skip()

def test_fail():
    try:
        deadbeef.get_string(10000)
        assert False
    except deadbeef.BADC0DE:
        assert True

if __name__ == '__main__':
    test_count()
    test_string()
    test_int()
    test_filters()
    test_skip()
    test_fail()
