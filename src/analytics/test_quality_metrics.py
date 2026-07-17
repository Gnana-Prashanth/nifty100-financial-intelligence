from quality_metrics import cfo_pat_ratio


def test_normal_case():
    assert cfo_pat_ratio(120, 100) == 1.2


def test_equal():
    assert cfo_pat_ratio(100, 100) == 1.0


def test_zero_profit():
    assert cfo_pat_ratio(100, 0) is None


def test_negative_profit():
    assert cfo_pat_ratio(80, -40) == -2.0


