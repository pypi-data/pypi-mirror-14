


def lowerbound_from(model):
    """Return the lowerbound found in given model, or MINIMAL_SCORE if not found"""
    lowbound = next(a for a in model if a.startswith('maxlowerbound('))
    assert len(lowbound) <= 1  # multiple maxlowerbound is impossible
    # the string 'inf' is the ASP type for 'infinitely small'
    # so, if no lowerbound found, 'inf' will be returned and
    # can't be converted in integer
    try:
        lowbound_value = atoms.first_arg(lowbound[0])
    except (IndexError, ValueError):  # if no lowbound or infinite lowbound
        lowbound_value = MINIMAL_SCORE
    return lowbound_value


def preprocessed_atoms(input_atoms, cc):
    """Return all the preprocessed atoms, or None if no model"""
    return solving_model_from(
        base_atoms=(input_atoms),
        aspfiles=asp_preprocessing,
        aspargs={ASP_ARG_CC: cc}
    )


def model_score(model):
    """Return the score of given model, or None if no score found inside"""
    score = int(atoms.first_arg(next(a for a in model
                                     if a.startswith('score('))))
    return score


def find_best_concept(input_atoms, cc, step, clique, lowerbound, last_score):
    """Search and return a model describing the best (bi)clique.

    input_atoms: all atoms that needs to be grounded
    cc: considered connected component
    step: the step number
    clique: flag, True if searching a clique, False for biclique
    lowerbound: minimal score allowed for the clique
    last_score: maximal score reachable by the clique

    return: an answer set describing the found clique, or None otherwise.

    """
    assert isinstance(step, int)
    assert isinstance(clique, bool)
    assert isinstance(lowerbound, int)
    assert isinstance(last_score, int)
    assert callable(notify_observers)
    # define data specific to clique or biclique
    asp_conceptfinder = asp_ccfinding if clique else asp_bcfinding
    # perform the solver call on data
    best_model = solving_model_from(
        base_atoms=input_atoms,
        aspfiles=(asp_conceptfinder, asp_postprocessing),
        aspargs={ASP_ARG_CC: cc, ASP_ARG_STEP: step,
                 ASP_ARG_LOWERBOUND: lowerbound,
                 ASP_ARG_UPPERBOUND: last_score}
    )
    # treatment of the model
    if model is not None:
        assert 'score' in str(model)
    return best_model
