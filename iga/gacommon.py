from pickle import loads
import random as rnd

#-------------------------------------------#
class CommonParams:
    '''
    Holder for shared variables.
    The variables are set and modified by the GUI.
    The vars are retrieved by the GA.
    '''

    def __init__(self):
        self.ga = None
        self.params = None
        self.app_name = None
        self.yaml_file = None
        self.dirty = False

#-------------------------------------------#
    def reset(self):
        '''
            Reset server state.
        '''
        self.exit()
        if self.ga:
            del self.ga
        self.ga = None
        self.params = None
        self.app_name = None
        self.yaml_file = None
        self.dirty = False

#-------------------------------------------#
    def getYaml(self):
        import yaml
        return yaml

#-------------------------------------------#
    def fileArgs(self, yaml_file):
        '''
        Parse config files.
        '''
        pre_path = yaml_file.split(yaml_file.split('/')[-1])[0]
        self.yaml_file = yaml_file
        yaml = self.getYaml()
        f = open(yaml_file, 'r')
        params = yaml.load(f)
        f.close()

        # helper func which recursively inherits dictionaries
        def fillDict(_params, _inherit_params):
            for _key, _value in _params.iteritems():
                if type(_value) is dict and _inherit_params.has_key(_key):
                    fillDict(_value, _inherit_params[_key])
                else:
                    _inherit_params[_key] = _value

        # parse any files from which the
        # yaml config is being inherited from
        if params.has_key('inherits'):
            inherit_params = {}
            base_files = params['inherits'][:]
            base_files.reverse()
            for filename in base_files:
                # fill temp dictionary with inherited attributes
                f = open(pre_path + filename, 'r')
                base_params = yaml.load(f)
                f.close()

                # values not defined in derived file are pulled from inherited file
                fillDict(inherit_params, base_params)
                inherit_params = base_params

            # fill our dictionary with values inherited
            fillDict(params, inherit_params)
            self.params = inherit_params                       
        else:
            self.params = params

        self.app_name = self.params['application']['name']
        if self.params['seed']:
            self.params['random'] = rnd.Random(self.params['seed'])
        else:
            self.params['random'] = rnd.Random()

#-------------------------------------------#
    def exit(self):
        '''
        Kill running server.
        '''
        if self.dirty:
            self.yaml_file
            f = open(self.yaml_file, 'r')
            params = f.readlines()
            f.close()

            f = open(self.yaml_file, 'w')
            for line in params:
                f.write(line)
            f.close()


#-------------------------------------------#
    def getGARates(self):
        '''
        Get crossover and mutation rates.
        '''
        return self.params['crossover']['prob'], self.params['mutation']['prob']

#-------------------------------------------#
    def setVar(self, name, value):
        '''
        Set variable in the attributes dictionary, or create new if var doesn't exist.
        directly.
        '''
        if name == 'crossover_prob':
            self.params['crossover']['prob'] = value
        elif name == 'mutation_prob':
            self.params['mutation']['prob'] = value
        elif name == 'population_size':
            self.params['population']['size'] = value
        else:
            self.params[name] = value


#-------------------------------------------#
    def setVars(self, varNames, values):
        '''
        Sets variables from list in the attributes dictionary, or create new if var doesn't exist.
        directly.
        '''
        for i in xrange(len(varNames)):
            self.params[varNames[i]] = values[i]

#-------------------------------------------#
    def getVar(self, name):
        '''
        Get variable from the attributes dictionary. To keep from accessing the dictionary
        directly.
        '''
        x = self.params
        g = self.ga
        app = self.app_name
        yf = self.yaml_file
        dirty = self.dirty
        if name == 'crossover_prob':
            return self.params['crossover']['prob']
        elif name == 'mutation_prob':
            return self.params['mutation']['prob']
        elif name == 'population_size':
            return self.params['population']['size']

        else:
            if self.params.has_key(name):
                return self.params[name]
            else:
                print 'Variable %s does not exist!' % name
                return None

#-------------------------------------------#
    def getVars(self, varNames):
        '''
        Get list of variables from the attributes dictionary. To keep from accessing the dictionary
        directly.
        '''
        returnList = []
        for name in varNames:
            if self.params.has_key(name):
                returnList.append(self.params[name])
            else:
                print 'Variable %s does not exist!' % name

        return returnList


#-------------------------------------------#
    def setArgs(self, args):
        '''
        Update settings based on command line arguments.
        Command line arguments override file defaults.
        '''
        if args:
            self.setVars(args.keys(), args.values())


#-------------------------------------------#
    def consoleGA(self):
        '''
        Run non-interactive GA.
        '''
        from ga import GA
        ga = GA(self.params)
        ga.run()
        return ga.getPop()

#-------------------------------------------#
    def onInit(self, context = {}):
        '''
        Called when GA is created.
        '''
        self.params['application']['init_context'] = context
        from iga import IGA
        self.ga = IGA(self.params)

#-------------------------------------------#
    def onRun(self, display_panel):
        '''
        Called when GA is created.
        '''
        from iga import IGA
        self.ga = IGA(self.params)

        return self.ga.run(display_panel)

#-------------------------------------------#
    def step(self, user_feedback, inject_genomes = None):
        '''
        Take the user input and the individuals to inject
        and step n generations.
        '''
        print 'user_feedback', user_feedback
        return self.ga.step(user_feedback, inject_genomes)

#-------------------------------------------#
    def old_draw(self, parent_panel, genomes):
        '''
        Take a list of genomes and have the app file
        create panels for them.
        '''
        panels = self.ga.draw(parent_panel, genomes)
        return panels

#-------------------------------------------#
    def getAppVars(self):
        '''
        Return a reference to the application variables.
        '''
        if self.params['application'].has_key('vars'):
            return self.params['application']['vars']
        else:
            return None

#-------------------------------------------#
    def back(self):
        return self.ga.back()

#-------------------------------------------#
    def getAppName(self):
        return self.app_name

#-------------------------------------------#
    def callAppSlot(self, slot, args):
        self.ga.callAppSlot(slot, args)


#-------------------------------------------#
    def getPop(self):
        '''
        Web method.
        '''
        return self.ga.getPop()

#-------------------------------------------#
    #def web_step(self, user_feedback, inject_genomes = None):
    def web_step(self, context = {}):
        '''
        Take the user input and the individuals to inject
        and step n generations.
        Web method.
        '''
        user_feedback = context.get('feedback', [])
        inject_genomes = context.get('inject_genomes', {})
        print 'user_feedback', user_feedback
        return self.ga.step(user_feedback, inject_genomes, context)

#-------------------------------------------#
    def draw(self, context = {}):
        '''
        Web method.
        '''
        return self.ga.igaStep(context)

#-------------------------------------------#
    def get_best(self, context):
        '''
        Web method.
        '''
        return self.ga.get_best(context)

#-------------------------------------------#
    def draw_peers(self, context):
        '''
        Web method.
        '''
        #panels = self.ga.draw(parent_panel, genomes)
        return self.ga.draw(context)

#-------------------------------------------#


gaParams = CommonParams()
