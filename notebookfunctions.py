from taxcalc.utils import add_quantile_bins


epsilon = 1e-9


def distribution(item, weight, agi):
    """
    Return distribution of item by AGI level
    """
    total = (item * weight).sum()
    agi_1 = ((item[agi < 0] * weight[agi < 0]).sum())
    pct1 = round(agi_1 / total, 2)
    agi_2 = ((item[(agi > 1) & (agi < 5000)] *
              weight[(agi > 1) & (agi < 5000)]).sum())
    pct2 = round(agi_1 / total, 2)
    agi_3 = ((item[(agi > 5000) & (agi < 10000)] *
              weight[(agi > 5000) & (agi < 10000)]).sum())
    pct3 = round(agi_3 / total, 2)
    agi_4 = ((item[(agi > 10000) & (agi < 15000)] *
              weight[(agi > 10000) & (agi < 15000)]).sum())
    pct4 = round(agi_4 / total, 2)
    agi_5 = ((item[(agi > 15000) & (agi < 20000)] *
              weight[(agi > 15000) & (agi < 20000)]).sum())
    pct5 = round(agi_5 / total, 2)
    agi_6 = ((item[(agi > 20000) & (agi < 25000)] *
              weight[(agi > 20000) & (agi < 25000)]).sum())
    pct6 = round(agi_6 / total, 2)
    agi_7 = ((item[(agi > 25000) & (agi < 30000)] *
              weight[(agi > 25000) & (agi < 30000)]).sum())
    pct7 = round(agi_7 / total, 2)
    agi_8 = ((item[(agi > 30000) & (agi < 40000)] *
              weight[(agi > 30000) & (agi < 40000)]).sum())
    pct8 = round(agi_8 / total, 2)
    agi_9 = ((item[(agi > 40000) & (agi < 50000)] *
              weight[(agi > 40000) & (agi < 50000)]).sum())
    pct9 = round(agi_9 / total, 2)
    agi_10 = ((item[(agi > 50000) & (agi < 75000)] *
               weight[(agi > 50000) & (agi < 75000)]).sum())
    pct10 = round(agi_10 / total, 2)
    agi_11 = ((item[(agi > 75000) & (agi < 100000)] *
               weight[(agi > 75000) & (agi < 100000)]).sum())
    pct11 = round(agi_11 / total, 2)
    agi_12 = ((item[(agi > 100000) & (agi < 200000)] *
               weight[(agi > 100000) & (agi < 200000)]).sum())
    pct12 = round(agi_12 / total, 2)
    agi_13 = ((item[(agi > 200000) & (agi < 500000)] *
               weight[(agi > 200000) & (agi < 500000)]).sum())
    pct13 = round(agi_13 / total, 2)
    agi_14 = ((item[(agi > 500000) & (agi < 1000000)] *
               weight[(agi > 500000) & (agi < 1000000)]).sum())
    pct14 = round(agi_14 / total, 2)
    agi_15 = ((item[(agi > 1000000) & (agi < 1500000)] *
               weight[(agi > 1000000) & (agi < 1500000)]).sum())
    pct15 = round(agi_15 / total, 2)
    agi_16 = ((item[(agi > 1500000) & (agi < 2000000)] *
               weight[(agi > 1500000) & (agi < 2000000)]).sum())
    pct16 = round(agi_16 / total, 2)
    agi_17 = ((item[(agi > 2000000) & (agi < 5000000)] *
               weight[(agi > 2000000) & (agi < 5000000)]).sum())
    pct17 = round(agi_17 / total, 2)
    agi_18 = ((item[(agi > 5000000) & (agi < 10000000)] *
               weight[(agi > 5000000) & (agi < 10000000)]).sum())
    pct18 = round(agi_18 / total, 2)
    agi_19 = (item[agi > 10000000] * weight[agi > 10000000]).sum()
    pct19 = round(agi_19 / total, 2)
    df = [agi_1, agi_2, agi_3, agi_4, agi_5, agi_6, agi_7, agi_8, agi_9,
          agi_10, agi_11, agi_12, agi_13, agi_14, agi_15, agi_16, agi_17,
          agi_18, agi_19]
    pct = [pct1, pct2, pct3, pct4, pct5, pct6, pct7, pct8, pct9, pct10, pct11,
           pct12, pct13, pct14, pct15, pct16, pct17, pct18, pct19]
    return df, pct


def index_list():
    index = ['Zero or Negative', '$1-$5K', '$5K-$10K', '$10K-$15K',
             '$15K-$20K', '$20K-$25K', '$25K-$30K', '$30K-$40K',
             '$40K-$50K', '$50K-$75K', '$75K-$100K', '$100K-$200K',
             '$200K-$500K', '$500K-$1M', '$1M-$1.5M', '$1.5M-$2M',
             '$2M-$5M', '$5M-$10M', '$10M and over']
    return index


def weighted_mean(pdf, col_name, wt_name='s006'):
    """
    Return weighted mean of col_name

    Parameters
    ----------
    pdf: Pandas DataFrame object
    col_name: variable to be averaged
    wt_name: weight
    """
    return (float((pdf[col_name] * pdf[wt_name]).sum()) /
            float(pdf[wt_name].sum() + epsilon))


def weighted_sum(pdf, col_name, wt_name='s006'):
    """
    Return weighted sum of col_name

    Parameters
    ----------
    pdf: Pandas DataFrame object
    col_name: variable to be averaged
    wt_name: weight
    """
    return (float((pdf[col_name] * pdf[wt_name]).sum()))


def percentile(pdf, col_name, num_bins, measure, income_wt=False,
               result_type='avg'):
    """
    """
    qpdf = add_quantile_bins(pdf, num_bins=num_bins,
                             income_measure=measure,
                             weight_by_income_measure=income_wt)
    gpdf = qpdf.groupby('bins', as_index=False)
    if result_type == 'avg':
        wpdf = gpdf.apply(weighted_mean, col_name)
    elif result_type == 'sum':
        wpdf = gpdf.apply(weighted_sum, col_name)
    else:
        msg = 'result_type must be "avg" or "sum"'
        raise ValueError(msg)
    return wpdf
