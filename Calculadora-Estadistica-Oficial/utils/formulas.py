import numpy as np
from scipy import stats
import math


def expected_value(values, probs):
    return sum(v * p for v, p in zip(values, probs))


def variance(values, probs):
    mu = expected_value(values, probs)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probs))


def std_deviation(values, probs):
    return math.sqrt(variance(values, probs))


def binomial_prob(n, k, p):
    return stats.binom.pmf(k, n, p)


def binomial_cumulative(n, k, p):
    return stats.binom.cdf(k, n, p)


def binomial_mean(n, p):
    return n * p


def binomial_variance(n, p):
    return n * p * (1 - p)


def poisson_prob(lam, k):
    return stats.poisson.pmf(k, lam)


def poisson_cumulative(lam, k):
    return stats.poisson.cdf(k, lam)


def normal_prob(x, mu, sigma):
    return stats.norm.cdf(x, mu, sigma)


def normal_prob_between(a, b, mu, sigma):
    return stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma)


def normal_z_score(x, mu, sigma):
    return (x - mu) / sigma


def normal_inverse(prob, mu, sigma):
    return stats.norm.ppf(prob, mu, sigma)


def standard_error_mean(sigma, n):
    return sigma / math.sqrt(n)


def standard_error_proportion(p, n):
    return math.sqrt(p * (1 - p) / n)


def sample_mean(data):
    return np.mean(data)


def sample_variance(data):
    return np.var(data, ddof=1)


def sample_std_dev(data):
    return np.std(data, ddof=1)


def sample_proportion(x, n):
    return x / n


def confidence_interval_mean_z(data, sigma, confidence):
    x_bar = sample_mean(data)
    n = len(data)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    me = z * sigma / math.sqrt(n)
    return x_bar, x_bar - me, x_bar + me, me


def confidence_interval_mean_z_from_stats(x_bar, sigma, n, confidence):
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    me = z * sigma / math.sqrt(n)
    return x_bar - me, x_bar + me, me


def confidence_interval_proportion(x, n, confidence):
    p_hat = x / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    me = z * math.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat, p_hat - me, p_hat + me, me


def confidence_interval_t(data, confidence):
    x_bar = sample_mean(data)
    s = sample_std_dev(data)
    n = len(data)
    t = stats.t.ppf(1 - (1 - confidence) / 2, n - 1)
    me = t * s / math.sqrt(n)
    return x_bar, x_bar - me, x_bar + me, me


def confidence_interval_t_from_stats(x_bar, s, n, confidence):
    t = stats.t.ppf(1 - (1 - confidence) / 2, n - 1)
    me = t * s / math.sqrt(n)
    return x_bar - me, x_bar + me, me


def sample_size_mean(sigma, e, confidence):
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    return math.ceil((z * sigma / e) ** 2)


def sample_size_proportion(p_guess, e, confidence):
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    return math.ceil(z ** 2 * p_guess * (1 - p_guess) / e ** 2)


def z_test_mean(x_bar, mu0, sigma, n, tail="two"):
    z = (x_bar - mu0) / (sigma / math.sqrt(n))
    if tail == "two":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif tail == "left":
        p_value = stats.norm.cdf(z)
    else:
        p_value = 1 - stats.norm.cdf(z)
    return z, p_value


def z_test_proportion(p_hat, p0, n, tail="two"):
    z = (p_hat - p0) / math.sqrt(p0 * (1 - p0) / n)
    if tail == "two":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif tail == "left":
        p_value = stats.norm.cdf(z)
    else:
        p_value = 1 - stats.norm.cdf(z)
    return z, p_value


def t_test_mean(x_bar, mu0, s, n, tail="two"):
    t = (x_bar - mu0) / (s / math.sqrt(n))
    df = n - 1
    if tail == "two":
        p_value = 2 * (1 - stats.t.cdf(abs(t), df))
    elif tail == "left":
        p_value = stats.t.cdf(t, df)
    else:
        p_value = 1 - stats.t.cdf(t, df)
    return t, p_value, df


def two_sample_z_test(x1_bar, x2_bar, sigma1, sigma2, n1, n2, tail="two"):
    z = (x1_bar - x2_bar) / math.sqrt(sigma1 ** 2 / n1 + sigma2 ** 2 / n2)
    if tail == "two":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif tail == "left":
        p_value = stats.norm.cdf(z)
    else:
        p_value = 1 - stats.norm.cdf(z)
    return z, p_value


def two_sample_t_test(x1_bar, x2_bar, s1, s2, n1, n2, tail="two"):
    sp2 = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
    sp = math.sqrt(sp2)
    t = (x1_bar - x2_bar) / (sp * math.sqrt(1 / n1 + 1 / n2))
    df = n1 + n2 - 2
    if tail == "two":
        p_value = 2 * (1 - stats.t.cdf(abs(t), df))
    elif tail == "left":
        p_value = stats.t.cdf(t, df)
    else:
        p_value = 1 - stats.t.cdf(t, df)
    return t, p_value, df, sp


def paired_t_test(before, after, tail="two"):
    d = np.array(after) - np.array(before)
    d_bar = np.mean(d)
    s_d = np.std(d, ddof=1)
    n = len(d)
    t = d_bar / (s_d / math.sqrt(n))
    df = n - 1
    if tail == "two":
        p_value = 2 * (1 - stats.t.cdf(abs(t), df))
    elif tail == "left":
        p_value = stats.t.cdf(t, df)
    else:
        p_value = 1 - stats.t.cdf(t, df)
    return t, p_value, df, d_bar, s_d


def linear_regression(x, y):
    n = len(x)
    x_bar = np.mean(x)
    y_bar = np.mean(y)
    Sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    Sxx = sum((xi - x_bar) ** 2 for xi in x)
    Syy = sum((yi - y_bar) ** 2 for yi in y)
    b1 = Sxy / Sxx
    b0 = y_bar - b1 * x_bar
    y_pred = [b0 + b1 * xi for xi in x]
    SSE = sum((yi - yhat) ** 2 for yi, yhat in zip(y, y_pred))
    s2 = SSE / (n - 2)
    s = math.sqrt(s2)
    se_b1 = s / math.sqrt(Sxx)
    t_b1 = b1 / se_b1
    p_value_b1 = 2 * (1 - stats.t.cdf(abs(t_b1), n - 2))
    r = Sxy / math.sqrt(Sxx * Syy)
    r2 = r ** 2
    return {
        "b0": b0,
        "b1": b1,
        "r": r,
        "r2": r2,
        "s": s,
        "se_b1": se_b1,
        "t_b1": t_b1,
        "p_value_b1": p_value_b1,
        "Sxx": Sxx,
        "Syy": Syy,
        "Sxy": Sxy,
        "SSE": SSE,
        "n": n,
        "x_bar": x_bar,
        "y_bar": y_bar,
        "y_pred": y_pred,
    }


def predict_regression(b0, b1, x_new):
    return b0 + b1 * x_new
