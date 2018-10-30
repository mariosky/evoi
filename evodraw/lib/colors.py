# -*- coding: utf-8 -*-
from operator import itemgetter

__author__ = 'mariosky'

import numpy
import random
from evodraw.lib.evospace import Population

import redis
import os
import json
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = "evoi.settings"

r = redis.Redis.from_url(settings.REDIS_URL)


def one_like(individual_id, user, timestamp, multiple=True):
    if multiple:
        user = user + ':' + str(timestamp)
    pipe = r.pipeline()
    if pipe.zadd(individual_id+':likes', user, timestamp):
        pipe.incr(individual_id+':views' )
        pipe.execute()
        return True
    else:
        return False

def rating(individual_id, rating, user, timestamp, multiple=True):
    if multiple:
        user = user + ':' + str(timestamp)
    pipe = r.pipeline()
    if pipe.zadd(individual_id+':ratings', rating , user):
        pipe.incr(individual_id+':views' )
        pipe.execute()
        return True
    else:
        return False


def get_likes(individual_id):
    return r.zcard(individual_id+':likes')


def get_views(individual_id):
    views = r.get(individual_id+':views')
    views = views or 0
    return int(views)


def one_view(individual_id,):
    r.incr( individual_id+':views' )


def current_fitness(fitness):
    return sum([fitness[k] for k in fitness])


def few_views(pop, views=2, count=2):
    return sum([1 for i in pop["sample"] if i["views"] >= views]) < count


def calc_fitness(pop):
    for ind in pop["sample"]:
        likes = get_likes(ind['id'])
        views = get_views(ind['id'])
        ind['likes']= likes
        ind['views'] = views
        ind['score'] = likes


def init_pop(populationSize, popName="pop", rangemin=0, rangemax=11, listSize=66):
    server = Population(popName)
    server.initialize()
    for individual in range(populationSize):
        chrome = [random.randint(rangemin, rangemax) for _ in range(listSize)]
        individual = {"id": None, "fitness": {"DefaultContext": 0.0}, "chromosome": chrome, "views": 0}
        server.put_individual(**individual)


def get_sample(population, size):
    evospace = Population(population)
    r = evospace.get_sample(size)
    return r


def take_sample(population, size):
    evospace = Population(population)
    r = evospace.take_sample(size)
    return r


def putback_sample(json_data, population):
    sample = None
    evospace = Population(population)
    if not isinstance(json_data, dict):
        sample = json.loads(json_data)
    else:
        sample = {'sample': json_data['sample'], 'sample_id': json_data['sample_id']}

    evospace.putback_sample(sample)


def crossVertical(papa, mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11, 6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11, 6)

    cut = random.randint(0, 10)
    if cut == 0:  # Si la dimension es 1
        papa_cut1 = papa["chromosome"][cut, :]
        mama_cut1 = mama["chromosome"][cut, :]
        papa_cut2 = papa["chromosome"][cut + 1:, :]
        mama_cut2 = mama["chromosome"][cut + 1:, :]

        child1 = numpy.vstack((papa_cut1[numpy.newaxis, :], mama_cut2))
        child2 = numpy.vstack((papa_cut2, mama_cut1[numpy.newaxis, :]))
    else:
        papa_cut1 = papa["chromosome"][:cut, :]
        mama_cut1 = mama["chromosome"][:cut, :]
        papa_cut2 = papa["chromosome"][cut:, :]
        mama_cut2 = mama["chromosome"][cut:, :]

        child1 = numpy.vstack((papa_cut1, mama_cut2))
        child2 = numpy.vstack((papa_cut2, mama_cut1))
    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child1.reshape(66).tolist(),
              'papa': papa["id"], 'mama': mama["id"],
              'crossover': 'crossVertical:' + str(cut)}

    child2 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child2.reshape(66).tolist(),
              'papa': papa["id"], 'mama': mama["id"],
              'crossover': 'crossVertical:' + str(cut)}
    return child1, child2


def crossHorizontal(papa, mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11, 6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11, 6)

    cut = random.randint(0, 5)

    if cut == 0:  # Si la dimension es 1
        papa_cut1 = papa["chromosome"][0:11, cut]
        mama_cut1 = mama["chromosome"][0:11, cut]
        papa_cut2 = papa["chromosome"][0:11, cut + 1:]
        mama_cut2 = mama["chromosome"][0:11, cut + 1:]
        child1 = numpy.hstack((papa_cut1[:, numpy.newaxis], mama_cut2))
        child2 = numpy.hstack((papa_cut2, mama_cut1[:, numpy.newaxis]))
    else:
        papa_cut1 = papa["chromosome"][0:11, 0:cut]
        mama_cut1 = mama["chromosome"][0:11, 0:cut]
        papa_cut2 = papa["chromosome"][0:11, cut:]
        mama_cut2 = mama["chromosome"][0:11, cut:]
        child1 = numpy.hstack((papa_cut1, mama_cut2))
        child2 = numpy.hstack((papa_cut2, mama_cut1))

    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child1.reshape(66).tolist(),
              'papa': papa["id"], 'mama': mama["id"],
              'crossover': 'crossHorizontal:' + str(cut)}

    child2 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child2.reshape(66).tolist(),
              'papa': papa["id"], 'mama': mama["id"],
              'crossover': 'crossHorizontal:' + str(cut)}

    return child1, child2


def crossMirrorH(papa, mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11, 6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11, 6)

    cut = random.randint(0, 2)

    papa_mirror = numpy.fliplr(papa["chromosome"])
    mama_mirror = numpy.fliplr(mama["chromosome"])

    child1 = numpy.hstack((papa["chromosome"][:, 0:5 - cut], papa_mirror[:, 5 - cut:6]))
    child2 = numpy.hstack((mama["chromosome"][:, 0:5 - cut], mama_mirror[:, 5 - cut:6]))

    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child1.reshape(66).tolist(),
              'papa': papa["id"], 'crossover': 'crossMirrorH:' + str(cut)}

    child2 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child2.reshape(66).tolist(),
              'mama': mama["id"], 'crossover': 'crossMirrorH:' + str(cut)}

    return child1, child2


def crossMirrorV(papa, mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11, 6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11, 6)

    cut = random.randint(0, 2)

    papa_mirror = numpy.flipud(papa["chromosome"])
    mama_mirror = numpy.flipud(mama["chromosome"])

    child1 = numpy.vstack((papa["chromosome"][0:10 - cut, :], papa_mirror[10 - cut:12, :]))
    child2 = numpy.vstack((mama["chromosome"][0:10 - cut, :], mama_mirror[10 - cut:12, :]))

    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child1.reshape(66).tolist(),
              'papa': papa["id"], 'crossover': 'crossMirrorV:' + str(cut)}

    child2 = {'id': None, 'fitness': {"DefaultContext": 0.0},
              'chromosome': child2.reshape(66).tolist(),
              'mama': mama["id"], 'crossover': 'crossMirrorV:' + str(cut)}

    return child1, child2


def mut_shuffle(individual):
    random.shuffle(individual["chromosome"])


def mut_replace(individual):
    replace = random.choice(individual["chromosome"])
    replace_to = random.choice(individual["chromosome"])
    print( replace, ">>", replace_to)
    individual["chromosome"] = [replace_to if x == replace else x for x in individual["chromosome"]]


def reprieve(individual):
    if len(individual["fitness"]) <= 2:
        return True
    else:
        return False


def evolve(sample_size=16):
    sample = get_sample(sample_size)
    pop = calc_fitness(sample)
    print(pop)
    if len([individual for individual in pop['sample'] if individual['currentFitness']]):
        pop["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    else:
        print ("Not possible")
        return None

    for i in pop["sample"]:
        print(i["id"], i["currentFitness"],)
        if "views" in i.keys():
            print(i["views"])

    offspring = pop["sample"][:sample_size / 2]
    out = pop["sample"][sample_size / 2:]

    # crossFunctions = [crossVertical]
    crossFunctions = [crossVertical, crossHorizontal, crossMirrorH, crossMirrorV, crossMirrorH, crossMirrorV]
    for papa, mama in zip(offspring[::2], offspring[1::2]):
        offspring1, offspring2 = random.choice(crossFunctions)(papa, mama)
        offspring1["views"] = 0
        offspring2["views"] = 0
        offspring.extend((offspring1, offspring1))

    print('############################')
    print(len(offspring), sample_size)
    print('############################')

    print('############################')

    putback_sample(sample["sample_id"], offspring)


def evolve_Tournament(sample_size=6, mutation_rate=0.3):
    # get two samples from evospace
    sample_papa = get_sample(sample_size)
    # if None evospace empty? just return
    if not sample_papa:
        return
    sample_mama = get_sample(sample_size)

    if not sample_mama:
        return

        # each must have a minimum of two individuals with at least 2 views each (DEFAULTS)
    # if not return both samples unchanged
    if few_views(sample_mama) or few_views(sample_papa):
        putback_sample(sample_mama["sample_id"], sample_mama["sample"])
        putback_sample(sample_papa["sample_id"], sample_papa["sample"])
        print ("few", few_views(sample_mama), few_views(sample_papa))
        return

    # Add currentFitness to individuals
    sample_papa = calc_fitness(sample_papa)
    sample_mama = calc_fitness(sample_mama)
    # get the best, first_parent
    sample_papa["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    papa = sample_papa["sample"][0]

    # get the best, second_parent
    sample_mama["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    mama = sample_mama["sample"][0]
    # crossFunctions = [crossVertical]
    crossFunctions = [crossVertical, crossHorizontal, crossMirrorH, crossMirrorV, crossMirrorH, crossMirrorV]

    offspring1, offspring2 = random.choice(crossFunctions)(papa, mama)
    offspring1["views"] = 0
    offspring2["views"] = 0
    print (offspring1)

    if random.random() <= mutation_rate:
        if random.random() <= .20:
            mut_shuffle(offspring1)
            mut_shuffle(offspring2)
            offspring1["mutation"] = "shuffle"
            offspring2["mutation"] = "shuffle"
            print ("shuffle")

        else:
            # range random?
            for i in range(random.randint(1, 4)):
                mut_replace(offspring1)
                mut_replace(offspring2)
                offspring1["mutation"] = "replace"
                offspring2["mutation"] = "replace"
            print ( "replace")

    worst_mama = min([a for a in sample_mama["sample"] if a["currentFitness"] is not None],
                     key=itemgetter('currentFitness'))
    worst_papa = min([a for a in sample_papa["sample"] if a["currentFitness"] is not None],
                     key=itemgetter('currentFitness'))
    sample_mama["sample"].remove(worst_mama)
    sample_papa["sample"].remove(worst_papa)

    sample_mama["sample"].append(offspring1)
    sample_papa["sample"].append(offspring2)

    putback_sample(sample_mama["sample_id"], sample_mama["sample"])
    putback_sample(sample_papa["sample_id"], sample_papa["sample"])


if __name__ == "__main__":
    init_pop(10)
    #evolve()