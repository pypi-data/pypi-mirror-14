from functools import reduce, partial


def stateless(initial_state, actions, dispatch):
    return reduce(lambda state, f: f(state), (dispatch[action] for action in actions), initial_state)


def statelesser(initial_state, actions, dispatch):
    return reduce(lambda state, f: f(state), (partial(dispatch[name], *args) for (name, args) in actions), initial_state)
