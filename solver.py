from copy import deepcopy


def pretty_format_env(env):
    """
    Args:
        env: a hash environment

    Returns:
        A pretty formatted env
    """
    s = []
    counter = 1
    for r in ["first", "second"]:
        for k in sorted(env[r].keys()):
            s.append("{:>12}".format("X{:02}: {:>5}".format(counter, env[r][k])))
            counter += 1
    return ",".join(s)


def _solve(mul, env, last, precedence, logging):
    if logging:
        print pretty_format_env(env)
    if mul.is_sufficient(env):
        if len(precedence) == last:
            return env
        for i in range(10):
            env_copy = deepcopy(env)
            env_copy[precedence[last][0]][precedence[last][1]] = i
            returned = _solve(mul, env_copy, last + 1, precedence, logging)
            if returned is not None:
                return returned
    else:
        return None


def solve(mul, logging=False):
    """
    Args:
        mul: a Multiplication instance

    Returns:
        A full sufficient environment. None if there's no such environment.
    """
    env = mul.configurable_env()
    unknowns_first = [("first", k, len(mul.first) - k) for k in env["first"].keys()]
    unknowns_second = [("second", k, len(mul.second) - k) for k in env["second"].keys()]
    precedence = sorted(unknowns_first + unknowns_second, key=lambda x: x[2])
    precedence = [(elem[0], elem[1]) for elem in precedence]
    if not precedence:
        return
    return _solve(mul, env, 0, precedence, logging)
