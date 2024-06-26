#from http://rosettacode.org/wiki/Probabilistic_choice#Python
#pythran export test(str?, int?)
#runas test()

import random, bisect

def probchoice(items, probs, bincount=1000):
    '''
    Splits the interval 0.0-1.0 in proportion to probs
    then finds where each random.random() choice lies
    '''

    prob_accumulator = 0
    accumulator = []
    for p in probs:
        prob_accumulator += p
        accumulator.append(prob_accumulator)

    while True:
        r = random.random()
        yield items[bisect.bisect(accumulator, r)]

def probchoice2(items, probs, bincount=1000):
    '''
    Puts items in bins in proportion to probs
    then uses random.choice() to select items.

    Larger bincount for more memory use but
    higher accuracy (on avarage).
    '''

    bins = []
    for item,prob in zip(items, probs):
        bins += [item]*int(bincount*prob)
    while True:
        yield random.choice(bins)


def tester(func=probchoice, items=('good', 'bad' 'ugly'),
        probs=(0.5, 0.3, 0.2),
        trials = 100000
        ):
    def problist2string(probs):
        '''
        Turns a list of probabilities into a string
        Also rounds FP values
        '''
        return ",".join('{:8.6f}'.format(p) for p in probs)

    counter = dict()
    it = func(items, probs)
    for dummy in range(trials):
        k = next(it)
        if k in counter:
            counter[k] += 1
        else:
            counter[k] = 1
    print("\n##\n##\n##")
    print("Trials:              ", trials)
    print("Items:               ", ' '.join(items))
    print("Target probability:  ", problist2string(probs))
    print("Attained probability:", problist2string(
        counter[x]/float(trials) for x in items))

def test(init_seq='aleph beth gimel daleth he waw zayin heth', bincount=1000000):
    items = init_seq.split()
    probs = [1/(float(n)+5) for n in range(len(items))]
    probs[-1] = 1-sum(probs[:-1])
    tester(probchoice, items, probs, bincount)
    tester(probchoice2, items, probs, 1000000)
