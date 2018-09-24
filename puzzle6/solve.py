#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from math import *
from random import Random

FILE = "voter.json"

data = json.load(open(FILE, "r"))
data = (data["voters_by_block"]["party_A"], data["voters_by_block"]["party_B"])
population = sum(data[0]) + sum(data[1])
n = 10
D = 20
SVP = .6  # straightVoteProbability
goalMetrics = (0, 11.0, 2.05e12, -0.14 * population)
weights = (1 / 40, -1 / 10, 1 / goalMetrics[2], 1 / goalMetrics[3] / population)
SEED = b'\x00\xc1\xba\xeb\xba\xd2\x89g\x952\xc6-\xdb\xc0\xb4\x8b'
ITERS = int(1e4)


def change(state, cell, newDistrict):
    ret = state.copy()
    ret[cell] = newDistrict
    return ret


def adjacent(cell):
    if cell % n > 0:
        yield cell - 1
    if cell % n < n - 1:
        yield cell + 1
    if cell >= n:
        yield cell - n
    if cell < n * n - n:
        yield cell + n


def neighbours(state):
    firstEmpty = next(iter(set(range(D)).difference(set(state))), None)
    for i in range(n * n):
        candidates = set()
        ownDistrict = state[i]
        NIS = [
            i >= n and state[i - n] == ownDistrict,
            i >= n and i % n > 0 and state[i - n - 1] == ownDistrict,
            i % n > 0 and state[i - 1] == ownDistrict,
            i < n * n - n and i % n > 0 and state[i + n - 1] == ownDistrict,
            i < n * n - n and state[i + n] == ownDistrict,
            i < n * n - n and i % n < n - 1 and state[i + n + 1] == ownDistrict,
            i % n < n - 1 and state[i + 1] == ownDistrict,
            i >= n and i % n < n - 1 and state[i - n + 1] == ownDistrict,
        ]
        if (NIS[0] and NIS[2] and not NIS[1]) or \
                (NIS[2] and NIS[4] and not NIS[3]) or \
                (NIS[4] and NIS[6] and not NIS[5]) or \
                (NIS[6] and NIS[0] and not NIS[7]) or \
                (NIS[0] and NIS[4] and not NIS[2] and not NIS[6]) or \
                (NIS[2] and NIS[6] and not NIS[0] and not NIS[4]):
            continue
        for neighbour in adjacent(i):
            candidates.add(state[neighbour])
        candidates.discard(ownDistrict)
        if firstEmpty is not None:
            candidates.add(firstEmpty)
        for candidate in candidates:
            yield change(state, i, candidate)


def evaluate(state):
    pops = [[0, 0] for i in range(D)]
    for district, aPop, bPop in zip(state, *data):
        pops[district][0] += aPop
        pops[district][1] += bPop

    hasEmpty = 0
    aDistricts = 0.
    DPI = 0.
    EEG = 0.

    for aVoters, bVoters in pops:
        if aVoters == 0 and bVoters == 0:
            hasEmpty += 1
            continue

        pWin = (1 + erf((aVoters * SVP + bVoters * (1 - SVP) - (aVoters + bVoters) / 2) / sqrt(
            2 * (aVoters + bVoters) * SVP * (1 - SVP)))) / 2
        aDistricts += pWin

        preDPI = aVoters + bVoters - population / D
        DPI += preDPI * preDPI

        EEG += 2 * (aVoters * SVP + bVoters * (1 - SVP)) - (aVoters + bVoters) * (pWin + 0.5)

    return hasEmpty, aDistricts, DPI, EEG


def energy(s):
    metrics = evaluate(s)
    x = sum(max(0, (current - goal) * weight) for current, goal, weight in zip(metrics, goalMetrics, weights))
    return x


def temperature(proportion):
    return 1 / (proportion * 5 + 0.01) - 1 / 5.01


def P(oldEnergy, newEnergy, temp):
    if newEnergy < oldEnergy:
        return 1
    else:
        return exp((oldEnergy - newEnergy) / temp)


def main():
    state = [0, ] * (n * n)
    rng = Random()
    rng.seed(SEED)
    currentEnergy = energy(state)
    for i in range(ITERS):
        temp = temperature(i / ITERS)
        if i % 25 == 0:
            print(i, currentEnergy, temp, evaluate(state))
        if currentEnergy <= 0:
            break
        nextState = rng.choice(list(neighbours(state)))
        nextStateEnergy = energy(nextState)
        if rng.random() < P(currentEnergy, nextStateEnergy, temp):
            state = nextState
            currentEnergy = nextStateEnergy

    print(evaluate(state))
    solution = [[] for i in range(D)]
    for block, district in enumerate(state):
        solution[district].append(block)
    print(json.dumps(solution))


if __name__ == "__main__":
    main()
