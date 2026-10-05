"""数学恒等式、跨语言对照与时间顺序检查。"""
import hashlib
import json
import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from common import ROOT, prices
from CH01.lesson import e_series
from CH02.lesson import returns
from CH03.lesson import capm_data
from CH05.lesson import simulate_garch
from CH07.lesson import local_linear
from CH08.lesson import equal_weight_factors
from CH10.lesson import ns_curves
from CH11.lesson import historical_risk, hill


def test_compounding_and_log_additivity():
    p = np.array([100., 50., 100., 110.])
    simple, log = returns(p)
    assert np.prod(1 + simple) - 1 == pytest.approx(p[-1] / p[0] - 1)
    assert log.sum() == pytest.approx(np.log(p[-1] / p[0]))
    assert simple[:2].mean() != pytest.approx(0.)
    assert e_series(30) == pytest.approx(np.e, abs=1e-14)


@pytest.mark.parametrize('p', [[100, 0], [100, -1], [100, np.inf], [1]])
def test_invalid_prices(p):
    with pytest.raises(ValueError):
        returns(p)


def test_price_csv_order_and_duplicates(tmp_path):
    file = tmp_path / 'price.csv'
    pd.DataFrame({'date': ['2024-01-03', '2024-01-02'], 'close': [11., 10.]}).to_csv(file, index=False)
    assert prices(file, minimum=2).close.tolist() == [10., 11.]
    pd.DataFrame({'date': ['2024-01-02'] * 2, 'close': [11., 10.]}).to_csv(file, index=False)
    with pytest.raises(ValueError, match='重复'):
        prices(file, minimum=2)


def test_R_mtcars_coefficients():
    d = pd.read_csv(ROOT / 'CH03/data/mtcars.csv')
    fit = sm.OLS(d.mpg * 1.609344 / 3.785411784, sm.add_constant(d.wt * .45359237)).fit()
    np.testing.assert_allclose(fit.params, [15.8515367707892, -5.00927398466384], atol=1e-11)


def test_R_CAPM_coefficients_and_missingness():
    r, flags = capm_data(ROOT / 'CH03/data/stock_data.csv')
    assert flags.interpolated.sum() == 12
    assert len(r) == 371
    fit = sm.OLS(r.stock_excess, sm.add_constant(r.market_excess)).fit()
    np.testing.assert_allclose(fit.params, [.000891339721692584, 1.26900615881141], atol=1e-12)
    np.testing.assert_allclose(fit.bse, [.000922648578303695, .0732712109909688], atol=1e-12)


def test_no_endpoint_extrapolation(tmp_path):
    d = pd.read_csv(ROOT / 'CH03/data/stock_data.csv')
    d.loc[0, 'stock_price'] = np.nan
    f = tmp_path / 'prices.csv'
    d.to_csv(f, index=False)
    with pytest.raises(ValueError):
        capm_data(f)


def test_GARCH_recursion():
    r, h = simulate_garch(n=200)
    np.testing.assert_allclose(h[1:], .01 + .05 * r[:-1] ** 2 + .9 * h[:-1], atol=1e-14)
    assert np.all(h > 0)
    with pytest.raises(ValueError):
        simulate_garch(alpha=.2, beta=.9)


def test_local_linear_reproduces_line():
    x = np.linspace(-2, 2, 100)
    grid = np.linspace(-1.8, 1.8, 10)
    np.testing.assert_allclose(local_linear(x, 2 + 3 * x, grid, .3), 2 + 3 * grid, atol=1e-12)


def test_factor_sort_uses_previous_period():
    rng = np.random.default_rng(91)
    mv = rng.uniform(10, 100, (20, 5)); pb = rng.uniform(1, 5, (20, 5)); r = rng.normal(size=(20, 5))
    base = equal_weight_factors(mv, pb, r)
    changed_mv = mv.copy(); changed_pb = pb.copy()
    changed_mv[:, 3] = mv[::-1, 3]; changed_pb[:, 3] = pb[::-1, 3]
    altered = equal_weight_factors(changed_mv, changed_pb, r)
    # Modifying period-4 characteristics cannot alter period-4 returns, only later portfolios.
    pd.testing.assert_series_equal(base.iloc[2], altered.iloc[2])
    assert not np.allclose(base.iloc[3][['SMB','HML']], altered.iloc[3][['SMB','HML']])


def test_NS_zero_limit_and_forward_identity():
    theta = [.03, -.02, .025, 2]
    d, y, f = ns_curves(np.array([0., 1e-10]), theta)
    assert d[0] == 1
    np.testing.assert_allclose(y, .01, atol=1e-10)
    t = np.array([.5, 2., 10.]); eps = 1e-5
    numerical = -(np.log(ns_curves(t + eps, theta)[0]) - np.log(ns_curves(t - eps, theta)[0])) / (2 * eps)
    np.testing.assert_allclose(numerical, ns_curves(t, theta)[2], atol=1e-10)


def test_ES_fractional_probability_and_translation():
    x = np.array([0., 1., 2., 10.])
    var, es = historical_risk(x, .6)
    assert var == 2
    assert es == pytest.approx((.15 * 2 + .25 * 10) / .4)
    shifted = historical_risk(x + 7, .6)
    np.testing.assert_allclose(shifted, [var + 7, es + 7])
    assert historical_risk([3, 3, 3], .99) == pytest.approx((3., 3.))
    with pytest.raises(ValueError):
        hill([1., 2., 3.], 3)


def test_dataset_integrity():
    for item in json.loads((ROOT / 'data_manifest.json').read_text()):
        assert hashlib.sha256((ROOT / item['file']).read_bytes()).hexdigest() == item['sha256']
