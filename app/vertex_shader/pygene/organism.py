"""
Implements classes for entire organisms

Organisms produce Gametes (think sperm/egg) via
the .split() method.

Organisms can be mated by the '+' operator, which
produces a child organism.

Subclasses of Organism must override the following methods:
    - fitness - returns a float value representing the
      organism's fitness - a value from 0.0 to infinity, where
      lower is better

Refer to module pygene.prog for organism classes for genetic
programming.
"""

from random import random, randrange, choice

from gene import BaseGene, rndPair
from gamete import Gamete

from xmlio import PGXmlMixin

class BaseOrganism(PGXmlMixin):
    """
    Base class for genetic algo and genetic programming
    organisms
    
    Best not use this directly, but rather use or subclass from
    one of:
        - Organism
        - MendelOrganism
        - ProgOrganism
    """
    def __add__(self, partner):
        """
        Allows '+' operator for sexual reproduction
    
        Returns a whole new organism object, whose
        gene pair for each gene name are taken as one
        gene randomly selected from each parent
        """
        return self.mate(partner)
    
    def mate(self, partner):
        """
        Mates this organism with another organism to
        produce an entirely new organism
    
        Override this in subclasses
        """
        raise Exception("method 'mate' not implemented")
    
    def fitness(self):
        """
        Return the fitness level of this organism, as a float
        
        Should return a number from 0.0 to infinity, where
        0.0 means 'perfect'
    
        Organisms should evolve such that 'fitness' converges
        to zero.
        
        This method must be overridden
        """
        raise Exception("Method 'fitness' not implemented")
    
    def duel(self, opponent):
        """
        Duels this organism against an opponent
        
        Returns -1 if this organism loses, 0 if it's
        a tie, or 1 if this organism wins
        """
        #print "BaseOrganism.duel: opponent=%s" % str(opponent)
    
        return cmp(self.fitness(), opponent.fitness())
    
    def __cmp__(self, other):
        """
        Convenience method which invokes duel
        
        Allows lists of organisms to be sorted
        """
        return self.duel(other)
    
    def __repr__(self):
        """
        Delivers a minimal string representation
        of this organism.
        
        Override if needed
        """
        return "<%s:%s>" % (self.__class__.__name__, self.fitness())
    
    def mutate(self):
        """
        Implement the mutation phase
    
        Must be overridden
        """
        raise Exception("method 'mutate' not implemented")
    
    def dump(self):
        """
        Produce a detailed human-readable report on
        this organism and its structure
        """
        raise Exception("method 'dump' not implemented")
    
    def xmlDumpSelf(self, doc, parent):
        """
        Dumps out this object's contents into an xml tree
        
        Arguments:
            - doc - an xml.dom.minidom.Document object
            - parent - an xml.dom.minidom.Element parent, being
              the node into which this node should be placed
        """
        raise Exception("method xmlDumpSelf not implemented")
    
    def xmlDumpAttribs(self, elem):
        """
        Dump out the custom attributes of this
        organism
        
        elem is an xml.dom.minidom.element object
        """

class Organism(BaseOrganism):
    """
    Simple genetic algorithms organism

    Contains only single genes, not pairs (ie, single-helix)
    
    Note - all organisms are hermaphrodites, which
    can reproduce by mating with another.
    In this implementation, there is no gender.

    Class variables (to override) are:
        - genome - a dict mapping gene names to gene classes

        - mutateOneOnly - default False - dictates whether mutation
          affects one randomly chosen gene unconditionally, or
          all genes subject to the genes' individual mutation settings

        - crossoverRate - default .5 - proportion of genes to
          split out to first child in each pair resulting from
          a mating

    Python operators supported:
        - + - mates two organism instances together, producing a child
        - [] - returns the value of the gene of a given name
        - <, <=, >, >= - compares fitness value to that of another instance
    """
    # dict which maps genotype names to gene classes
    genome = {}
    
    # dictates whether mutation affects one randomly chosen
    # gene unconditionally, or all genes subject to the genes'
    # own mutation settings
    
    mutateOneOnly = False
    
    # proportion of genes to split out to first
    # child
    crossoverRate = 0.5
    
    def __init__(self, **kw):
        """
        Initialises this organism randomly,
        or from a set of named gene keywords
    
        Arguments:
            - gamete1, gamete2 - a pair of gametes from which
              to take the genes comprising the new organism.
              May be omitted.
        
        Keywords:
            - keyword names are gene names within the organism's
              genome, and values are either:
                  - instances of a Gene subclass, or
                  - a Gene subclass (in which case the class will
                    be instantiated to form a random gene object)
    
        Any gene names in the genome, which aren't given in the
        constructor keywords, will be added as random instances
        of the respective gene class. (Recall that all Gene subclasses
        can be instantiated with no arguments to create a random
        valued gene).
        """
        # the set of genes which comprise this organism
        self.genes = {}
    
        # remember the gene count
        self.numgenes = len(self.genome)
    
        # we're being fed a set of zero or more genes
        for name, cls in self.genome.items():
    
            # set genepair from given arg, or default to a
            # new random instance of the gene
            gene = kw.get(name, cls)
    
            # if we're handed a gene class instead of a gene object
            # we need to instantiate the gene class
            # to form the needed gene object
            try:
                if issubclass(gene, BaseGene):
                    gene = gene()
            except:
                pass
    
            # either way, we should have a valid gene now
    
            # validate the gene
            if not isinstance(gene, BaseGene):
                raise Exception(
                    "object given as gene %s %s is not a gene" % (
                        name, repr(gene)))
    
            # all good - add in the gene to our genotype
            self.genes[name] = gene
    
    def copy(self):
        """
        returns a deep copy of this organism
        """
        genes = {}
        for name, gene in self.genes.items():
            genes[name] = gene.copy()
        return self.__class__(**genes)
    
    def mate(self, partner):
        """
        Mates this organism with another organism to
        produce two entirely new organisms via random choice
        of genes from this or the partner
        """
        genotype1 = {}
        genotype2 = {}
    
        # gene by gene, we assign our and partner's genes randomly
        for name, cls in self.genome.items():
            
            ourGene = self.genes.get(name, None)
            if not ourGene:
                ourGene = cls()
    
            partnerGene = self.genes.get(name, None)
            if not partnerGene:
                partnerGene = cls()
                
            # randomly assign genes to first or second child
            if random() < self.crossoverRate:
                genotype1[name] = ourGene
                genotype2[name] = partnerGene
            else:
                genotype1[name] = partnerGene
                genotype2[name] = ourGene
        
        # got the genotypes, now create the child organisms
        child1 = self.__class__(**genotype1)
        child2 = self.__class__(**genotype2)
    
        # done
        return (child1, child2)
    
    def __getitem__(self, item):
        """
        allows shorthand for querying the phenotype
        of this organism
        """
        return self.genes[item].value
    
    def phenotype(self, geneName=None):
        """
        Returns the phenotype resulting from a
        given gene, OR the total phenotype resulting
        from all the genes
        
        tries to invoke a child class' method
        called 'phen_<name>'
        """
        # if no gene name specified, build up an entire
        # phenotype dict
        if geneName == None:
            phenotype = {}
            for name, cls in self.genome.items():
                val = self.phenotype(name)
                if not phenotype.has_key(name):
                    phenotype[name] = []
                phenotype[name].append(val)
    
            # got the whole phenotype now
            return phenotype
    
        # just getting the phenotype for one gene pair
        return self.genes[geneName]
    
    def mutate(self):
        """
        Implement the mutation phase, invoking
        the stochastic mutation method on each
        component gene
        
        Does not affect this organism, but returns a mutated
        copy of it
        """
        mutant = self.copy()
        
        if self.mutateOneOnly:
            # unconditionally mutate just one gene
            gene = choice(mutant.genes.values())
            gene.mutate()
    
        else:
            # conditionally mutate all genes
            for gene in mutant.genes.values():
                gene.maybeMutate()
    
        return mutant
    
    def dump(self):
        """
        Produce a detailed human-readable report on
        this organism, its genotype and phenotype
        """
        print "Organism %s:" % self.__class__.__name__
    
        print "  Fitness: %s" % self.fitness()
        for k,v in self.genes.items():
            print "  Gene: %s = %s" % (k, v)
    
    def xmlDumpSelf(self, doc, parent):
        """
        Dumps out this object's contents into an xml tree
        
        Arguments:
            - doc - an xml.dom.minidom.Document object
            - parent - an xml.dom.minidom.Element parent, being
              the node into which this node should be placed
        """
        orgtag = doc.createElement("organism")
        parent.appendChild(orgtag)
    
        self.xmlDumpClass(orgtag)
    
        self.xmlDumpAttribs(orgtag)
    
        # now dump out the constituent genes
        for name, cls in self.genome.items():
    
            # create a named genepair tag to contain genes
            pairtag = doc.createElement("genepair")
            orgtag.appendChild(pairtag)
            
            pairtag.setAttribute("name", name)
            
            # now write out genes
            gene = self.genes[name]
            #print "self.genes[%s] = %s" % (
            #    name,
            #    pair.__class__
            #    )
            gene.xmlDumpSelf(doc, pairtag)
    

class MendelOrganism(BaseOrganism):
    """
    Classical Mendelian genetic organism
    
    Contains a pair of genes for each gene in the genome

    Organisms contain a set of pairs of genes, where the
    genes of each pair must be of the same type.

    Class variables (to override) are:
        - genome - a dict mapping gene names to gene classes

        - mutateOneOnly - default False - if set, then the
          mutation phase will mutate exactly one of the genepairs
          in the genotype, randomly selected. If False, then
          apply mutation to all genes, subject to individual genes'
          mutation settings

    Python operators supported:
        - + - mates two organism instances together, producing a child
        - [] - returns the phenotype produced by the gene pair of a given name
        - <, <=, >, >= - compares fitness value to that of another instance
    """
    # dict which maps genotype names to gene classes
    genome = {}
    
    # dictates whether mutation affects one randomly chosen
    # gene unconditionally, or all genes subject to the genes'
    # own mutation settings
    
    mutateOneOnly = False
    
    def __init__(self, gamete1=None, gamete2=None, **kw):
        """
        Initialises this organism from either two gametes,
        or from a set of named gene keywords
    
        Arguments:
            - gamete1, gamete2 - a pair of gametes from which
              to take the genes comprising the new organism.
              May be omitted.
        
        Keywords:
            - keyword names are gene names within the organism's
              genome, and values are either:
                  - a tuple containing two instances of a Gene
                    subclass, or
                  - a Gene subclass (in which case the class will
                    be instantiated twice to form a random gene pair)
    
        Any gene names in the genome, which aren't given in the
        constructor keywords, will be added as random instances
        of the respective gene class. (Recall that all Gene subclasses
        can be instantiated with no arguments to create a random
        valued gene).
        """
        # the set of genes which comprise this organism
        self.genes = {}
    
        # remember the gene count
        self.numgenes = len(self.genome)
    
        if gamete1 and gamete2:
            # create this organism from sexual reproduction
            for name, cls in self.genome.items():
                self.genes[name] = (
                    gamete1[name].copy(),
                    gamete2[name].copy(),
                    )
    
            # and apply mutation
            #self.mutate()
    
            # done, easy as that
            return
    
        # other case - we're being fed a set of zero or more genes
        for name, cls in self.genome.items():
    
            # set genepair from given arg, or default to a
            # new random instance of the gene
            genepair = kw.get(name, cls)
    
            # if we're handed a gene class instead of a tuple
            # of 2 genes, we need to instantiate the gene class
            # to form the needed tuple
            try:
                if issubclass(genepair, BaseGene):
                    genepair = rndPair(genepair)
            except:
                pass
    
            # either way, we should have a valid gene pair now
    
            # validate the gene pair
            try:
                gene1, gene2 = genepair
            except:
                raise TypeError(
                    "constructor keyword values must be tuple of 2 Genes")
    
            if not isinstance(gene1, BaseGene):
                raise Exception(
                    "object %s is not a gene" % repr(gene1))
            if not isinstance(gene1, BaseGene):
                raise Exception(
                    "object %s is not a gene" % repr(gene2))
    
            # all good - add in the gene pair to our genotype
            self.genes[name] = genepair
    
    def copy(self):
        """
        returns a deep copy of this organism
        """
        genes = {}
        for name, genepair in self.genes.items():
            genes[name] = (genepair[0].copy(), genepair[1].copy())
        return self.__class__(**genes)
    
    def split(self):
        """
        Produces a Gamete object from random
        splitting of component gene pairs
        """
        genes1 = {}
        genes2 = {}
    
        for name, cls in self.genome.items():
    
            # fetch the pair of genes of that name
            genepair = self.genes[name]
    
            if randrange(0,2):
                genes1[name] = genepair[0]
                genes2[name] = genepair[1]
            else:
                genes1[name] = genepair[1]
                genes2[name] = genepair[0]
    
            # and pick one randomly
            #genes[name] = choice(genepair)
    
        gamete1 = Gamete(self.__class__, **genes1)
        gamete2 = Gamete(self.__class__, **genes2)
        
        return (gamete1, gamete2)
    
    def mate(self, partner):
        """
        Mates this organism with another organism to
        produce two entirely new organisms via mendelian crossover
        """
        #return self.split() + partner.split()
        ourGametes = self.split()
        partnerGametes = partner.split()
        child1 = self.__class__(ourGametes[0], partnerGametes[1])
        child2 = self.__class__(ourGametes[1], partnerGametes[0])
        return (child1, child2)
    
        # old single-child impl
        child = self.__class__(self.split(), partner.split())
        # look what the stork brought in!
        return child
    
    def __getitem__(self, item):
        """
        allows shorthand for querying the phenotype
        of this organism
        """
        return self.phenotype(item)
    
    def phenotype(self, geneName=None):
        """
        Returns the phenotype resulting from a
        given gene, OR the total phenotype resulting
        from all the genes
        
        tries to invoke a child class' method
        called 'phen_<name>'
        """
        # if no gene name specified, build up an entire
        # phenotype dict
        if geneName == None:
            phenotype = {}
            for name, cls in self.genome.items():
                val = self.phenotype(name)
                if not phenotype.has_key(name):
                    phenotype[name] = []
                phenotype[name].append(val)
    
            # got the whole phenotype now
            return phenotype
    
        # just getting the phenotype for one gene pair
    
        if not isinstance(geneName, str):
            geneName = str(geneName)
    
        try:
            #return sum(self.genes[geneName])
            genes = self.genes[geneName]
            return genes[0] + genes[1]
        except:
            #print "self.genes[%s] = %s" % (geneName, self.genes[geneName])
            raise
    
        # get the genes in question
        gene1, gene2 = self.genes[geneName]
    
        # try to find a specialised phenotype
        # calculation method
        methname = 'phen_' + geneName
        meth = getattr(self, methname, None)
    
        if meth:
            # got the method - invoke it
            return meth(gene1, gene2)
        else:
            # no specialised methods, apply the genes'
            # combination methods
            return gene1 + gene2
    
    def mutate(self):
        """
        Implement the mutation phase, invoking
        the stochastic mutation method on each
        component gene
        
        Does not affect this organism, but returns a mutated
        copy of it
        """
        mutant = self.copy()
        
        if self.mutateOneOnly:
            # unconditionally mutate just one gene
            genepair = choice(mutant.genes.values())
            for gene in genepair:
                gene.mutate()
    
        else:
            # conditionally mutate all genes
            for genepair in mutant.genes.values():
                for gene in genepair:
                    gene.maybeMutate()
    
        return mutant
    
    def dump(self):
        """
        Produce a detailed human-readable report on
        this organism, its genotype and phenotype
        """
        print "Organism %s:" % self.__class__.__name__
    
        print "  Fitness: %s" % self.fitness()
        for k,v in self.genes.items():
            print "  Gene: %s" % k
            print "    Phenotype: %s" % self[k]
            print "    Genotype:"
            print "      %s" % v[0]
            print "      %s" % v[1]
    
    def xmlDumpSelf(self, doc, parent):
        """
        Dumps out this object's contents into an xml tree
        
        Arguments:
            - doc - an xml.dom.minidom.Document object
            - parent - an xml.dom.minidom.Element parent, being
              the node into which this node should be placed
        """
        orgtag = doc.createElement("organism")
        parent.appendChild(orgtag)
    
        self.xmlDumpClass(orgtag)
    
        self.xmlDumpAttribs(orgtag)
    
        # now dump out the constituent genes
        for name, cls in self.genome.items():
    
            # create a named genepair tag to contain genes
            pairtag = doc.createElement("genepair")
            orgtag.appendChild(pairtag)
            
            pairtag.setAttribute("name", name)
            
            # now write out genes
            pair = self.genes[name]
            #print "self.genes[%s] = %s" % (
            #    name,
            #    pair.__class__
            #    )
            for gene in pair:
                gene.xmlDumpSelf(doc, pairtag)
    


