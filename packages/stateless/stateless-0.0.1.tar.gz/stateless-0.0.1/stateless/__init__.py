from functools import reduce


def stateless(initial_state, actions, dispatch):
    return reduce(lambda state, f: f(state), (dispatch[action] for action in actions), initial_state)
