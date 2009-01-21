
class Parameters:
    def __init__(self, params):

        self.params = params
        self.random = params['random']

        rnd = params['random']
        self.numgen = params['numgen']
        self.crossover = Crossover(params['crossover'], rnd)
        self.mutate = Mutation(params['mutation'], rnd)

        appname = params['application']['name']
        execstr = 'from app.%s.%s import %s as appclass' % (appname, appname, appname.capitalize())
        exec(execstr)
        self.app = appclass(params['application'], rnd)

        poptype = params['population']['type']
        execstr = 'from population.%s import Population as popclass' % (poptype)
        exec(execstr)
        self.pop = popclass(self, params['population'])



class Crossover:
    def __init__(self, params, rand):
        self.random = rand
        self.params = params
        self.points = params['points']
        self.prob = params['prob']

        funcname = params['type']
        execstr = 'from xo.%s import crossover as func' % (funcname)
        exec(execstr)
        self._func = func

    def __call__(self, p1, p2, extra_params = None):
        if extra_params:
            return self._func(p1, p2, self.params['prob'], self.params, self.random, extra_params)
        else:
            return self._func(p1, p2, self.params['prob'], self.params, self.random)

class Mutation:
    def __init__(self, params, rand):
        self.params = params
        self.random = rand

        funcname = params['type']
        execstr = 'from mut.%s import mutation as func' % (funcname)
        exec(execstr)
        self._mutation = func

    def __call__(self, ind, rate = None):
        return self._mutation(ind, rate or self.params['prob'], self.params, self.random)
