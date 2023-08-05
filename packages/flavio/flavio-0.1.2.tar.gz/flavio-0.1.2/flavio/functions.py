"""Main functions for user interaction. All of these are imported into the
top-level namespace."""

import flavio
import numpy as np
from collections import OrderedDict

def np_prediction(obs_name, wc_obj, *args, **kwargs):
    """Get the central value of the new physics prediction of an observable.

    Parameters
    ----------

    - `obs_name`: name of the observable as a string
    - `wc_obj`: an instance of `flavio.WilsonCoefficients`

    Additional arguments are passed to the observable and are necessary,
    depending on the observable (e.g. $q^2$-dependent observables).
    """
    obs = flavio.classes.Observable.get_instance(obs_name)
    return obs.prediction_central(flavio.default_parameters, wc_obj, *args, **kwargs)

def sm_prediction(obs_name, *args, **kwargs):
    """Get the central value of the Standard Model prediction of an observable.

    Parameters
    ----------

    - `obs_name`: name of the observable as a string

    Additional arguments are passed to the observable and are necessary,
    depending on the observable (e.g. $q^2$-dependent observables).
    """
    obs = flavio.classes.Observable.get_instance(obs_name)
    wc_sm = flavio.WilsonCoefficients()
    return obs.prediction_central(flavio.default_parameters, wc_sm, *args, **kwargs)

def sm_uncertainty(obs_name, *args, N=100, **kwargs):
    """Get the uncertainty of the Standard Model prediction of an observable.

    Parameters
    ----------

    - `obs_name`: name of the observable as a string
    - `N` (optional): number of random evaluations of the observable.
    The relative accuracy of the uncertainty returned is given by $1/\sqrt{2N}$.

    Additional arguments are passed to the observable and are necessary,
    depending on the observable (e.g. $q^2$-dependent observables).
    """
    obs = flavio.classes.Observable.get_instance(obs_name)
    wc_sm = flavio.WilsonCoefficients()
    par_random = [flavio.default_parameters.get_random_all() for i in range(N)]
    all_pred = np.array([
        obs.prediction_par(par, wc_sm, *args, **kwargs)
        for par in par_random
    ])
    return np.std(all_pred)

def sm_error_budget(obs_name, *args, N=50, **kwargs):
    """Get the *relative* uncertainty of the Standard Model prediction due to
    variation of individual observables.

    Parameters
    ----------

    - `obs_name`: name of the observable as a string
    - `N` (optional): number of random evaluations of the observable.
    The relative accuracy of the uncertainties returned is given by $1/\sqrt{2N}$.

    Additional arguments are passed to the observable and are necessary,
    depending on the observable (e.g. $q^2$-dependent observables).
    """
    obs = flavio.classes.Observable.get_instance(obs_name)
    wc_sm = flavio.WilsonCoefficients()
    par_central = flavio.default_parameters.get_central_all()
    par_random = [flavio.default_parameters.get_random_all() for i in range(N)]

    # Step 1: determine the parameters the observable depends on at all.
    # to this end, compute the observables once for each parameter with a
    # random value for this parameter but central values for all other
    # parameters. If the prediction is equal to the central prediction, the
    # observable does not depend on the parameter!
    pred_central = obs.prediction_par(par_central, wc_sm, *args, **kwargs)
    dependent_par = []
    for k in par_central.keys():
        par_tmp = par_central.copy()
        par_tmp[k] = par_random[0][k]
        pred_tmp = obs.prediction_par(par_tmp, wc_sm, *args, **kwargs)
        if pred_tmp != pred_central:
            dependent_par.append(k)

    # Step 2: for each of the dependent parameters, determine the error
    # analogous to the sm_uncertainty function. Normalize to the central
    # prediction (so relative errors are returned)
    individual_errors = {}
    def make_par_random(key, par_random):
        par_tmp = par_central.copy()
        par_tmp[key] = par_random[key]
        return par_tmp
    for p in dependent_par:
        par_random_p = [make_par_random(p, pr) for pr in par_random]
        all_pred = np.array([
            obs.prediction_par(par, wc_sm, *args, **kwargs)
            for par in par_random_p
        ])
        individual_errors[p] = np.std(all_pred)/abs(pred_central)
    return individual_errors
