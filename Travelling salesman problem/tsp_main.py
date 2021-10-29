import itertools
import math
import sys
import time

import numpy as np

# GOAL: Try to find the shortest overall route between N<=24 european cities


def LoadData(file):
    dist_array = np.loadtxt(file)
    total_number_of_cities = dist_array.shape[0]
    return dist_array, total_number_of_cities


def ComputeTotalDist(dist_data, route):
    n = len(route)
    path = 0.0
    for i in range(n - 1):
        city = route[i]  # Current city index
        c_n = route[i + 1]  # Next city index
        path += dist_data[city, c_n]
    path += dist_data[c_n, route[0]]  # Distance to close route at start city
    return path


def BruteForceSearch(dist_data, route):
    if len(route) > 11:
        print("Brute Force search can't handle more cities than 11. Exiting...")
        sys.exit(0)
    permutation_list = list(itertools.permutations(route, len(route)))
    number_of_routes = len(permutation_list)
    best_path = ComputeTotalDist(dist_data, permutation_list[0])
    print("------------------------------------------")
    print("  Method: Brute Force")
    print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_path, np.int_(permutation_list[0]))
    t0 = time.clock()
    for i in range(1, number_of_routes):
        new_path = ComputeTotalDist(dist_data, permutation_list[i])
        if new_path < best_path:
            best_path = new_path
            print("Better path:   %.2f \t" % best_path, np.int_(permutation_list[i]))
    all_routes = math.factorial(len(route))
    print("Time taken:", time.clock() - t0, "number of routes checked:", all_routes)


def RandomSearch(dist_data, route, max_iter):
    average_path = 0.0
    iter_route = np.zeros(len(route))
    best_route = np.zeros(len(route))
    best_path = ComputeTotalDist(dist_data, route)
    best_route[:] = route[:]
    iter_route[:] = route[:]
    print("------------------------------------------")
    print("  Method: Random guesses")
    print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_path, np.int_(route))
    i = 0
    while i < max_iter:
        i += 1
        np.random.shuffle(iter_route)
        new_path = ComputeTotalDist(dist_data, iter_route)
        average_path += new_path
        if new_path < best_path:
            best_path = new_path
            best_route[:] = iter_route[:]
            print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    print("Average length of random path is", average_path / float(max_iter))


def GreedySearch(dist_data, route, return_routes=False):
    n = len(route)
    nn_iter = 0.0
    nn_index = 0
    worst_dist = np.max(dist_data) * 2
    best_path = ComputeTotalDist(dist_data, route)
    best_route = np.zeros(n)
    best_route[:] = route[:]
    if not return_routes:
        print("------------------------------------------")
        print("--Method: Greedy Search")
        print("------------------------------------------")
        # print("Starting path: %.2f \t" %best_path, np.int_(route))
    if return_routes:
        routes_list_for_return = []
    for i in range(n):  # Run through all starting cities
        new_route = []
        new_route.append(i)
        while len(new_route) < n:
            nn_best = worst_dist
            for j in range(n):
                if j in new_route:
                    continue
                last_city_index = new_route[-1]
                nn_iter = dist_data[last_city_index, j]  # Go to nearest neighbour
                if nn_iter < nn_best:
                    nn_best = nn_iter
                    nn_index = j
            new_route.append(nn_index)
        new_path = ComputeTotalDist(dist_data, new_route)
        if return_routes:
            routes_list_for_return.append(new_route)
        if new_path < best_path:
            best_path = new_path
            best_route[:] = new_route[:]
            if not return_routes:
                print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    if return_routes:
        return routes_list_for_return


def HillClimber(dist_data, route, max_iter, return_best=False):
    n = len(route)
    best_route = np.zeros(n)
    best_path = ComputeTotalDist(dist_data, route)
    best_route[:] = route[:]
    if not return_best:
        print("------------------------------------------")
        print("  Method: Hill Climb, (single)")
        print("------------------------------------------")
        # print("Starting path: %.2f \t" %best_path, np.int_(route))
    route_iter_best = np.zeros(n)
    route_iter_best[:] = best_route[:]
    path_iter_best = best_path
    quit_no_better_path = True
    count = 0
    new_route = np.zeros(n)
    while count < max_iter and quit_no_better_path:
        count += 1
        quit_no_better_path = False
        for i in range(n - 1):
            for j in range(i, n - 1):
                if i == j:
                    continue
                new_route[:] = best_route[:]
                new_route[i] = best_route[j]
                new_route[j] = best_route[i]
                new_path = ComputeTotalDist(dist_data, new_route)
                if new_path < path_iter_best:
                    path_iter_best = new_path
                    route_iter_best[:] = new_route[:]
                    quit_no_better_path = True
        if quit_no_better_path:
            best_route[:] = route_iter_best[:]
            best_path = path_iter_best
    if not return_best:
        print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    if return_best:
        return best_path, best_route, count


def HillClimberMaxSlow(dist_data, route, max_iter, return_best=False):
    n = len(route)
    best_route = np.zeros(n)
    best_path = ComputeTotalDist(dist_data, route)
    best_route[:] = route[:]
    if not return_best:
        print("------------------------------------------")
        print("  Method: Hill Climb Max Slow, (single)")
        print("  NB: Not finished")
        print("------------------------------------------")
        # print("Starting path: %.2f \t" %best_path, np.int_(route))
    route_iter_best = np.zeros(n)
    route_iter_best[:] = best_route[:]
    path_iter_best = best_path
    quit_no_better_path = True
    count = 0
    new_route = np.zeros(n)
    while count < max_iter and quit_no_better_path:
        count += 1
        quit_no_better_path = False
        for i in range(n - 1):
            for j in range(i, n - 1):
                if i == j:
                    continue
                new_route[:] = best_route[:]
                new_route[i] = best_route[j]
                new_route[j] = best_route[i]
                new_path = ComputeTotalDist(dist_data, new_route)
                if new_path > path_iter_best and new_path < best_path:
                    path_iter_best = new_path
                    route_iter_best[:] = new_route[:]
                    quit_no_better_path = True
                if np.abs(path_iter_best - path_iter_best) < 0.01:
                    if new_path < path_iter_best:
                        path_iter_best = new_path
                        route_iter_best[:] = new_route[:]
                        quit_no_better_path = True
        if quit_no_better_path:
            best_route[:] = route_iter_best[:]
            best_path = path_iter_best
    if not return_best:
        print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    if return_best:
        return best_path, best_route, count


def HillClimberRandInit(dist_data, route, max_iter, rand_inits=100):
    iter_route = np.zeros(len(route))
    iter_route[:] = route[:]
    best_overall_route = np.zeros(len(route))
    best_overall_path = ComputeTotalDist(dist_data, route)
    best_overall_route[:] = route[:]
    print("------------------------------------------")
    print("  Method: Hill Climb rand. inits.")
    print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_overall_path, np.int_(iter_route))
    count = 0
    new_path = 0
    new_route = np.zeros(len(route))
    while count < rand_inits:
        count += 1
        np.random.shuffle(iter_route)  # Create random starting route
        new_path, new_route, iterations = HillClimber(
            dist_data, iter_route, max_iter, True
        )
        if new_path < best_overall_path:
            best_overall_path = new_path
            best_overall_route[:] = new_route[:]
            print(
                "Better path:   %.2f \t" % best_overall_path,
                np.int_(best_overall_route),
                "run:",
                count,
                ", iter:",
                iterations,
            )


def HillClimberFromGreedy(dist_data, route, max_iter):
    iter_route = np.zeros(len(route))
    iter_route[:] = route[:]
    best_overall_route = np.zeros(len(route))
    best_overall_path = ComputeTotalDist(dist_data, route)
    best_overall_route[:] = route[:]
    print("------------------------------------------")
    print("  Method: Hill Climb greedy search. inits.")
    print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_overall_path, np.int_(iter_route))
    new_path = 0
    new_route = np.zeros(len(route))
    route_list = GreedySearch(dist_data, route, True)
    for iter_route in route_list:
        new_path, new_route = HillClimber(dist_data, iter_route, max_iter, True)
        if new_path < best_overall_path:
            best_overall_path = new_path
            best_overall_route[:] = new_route[:]
            print(
                "Better path:   %.2f \t" % best_overall_path,
                np.int_(best_overall_route),
            )


def TwoPassMetropolis(dist_data, route, max_iter, return_routes=False):
    n = len(route)
    best_route = np.zeros(n)
    best_path = ComputeTotalDist(dist_data, route)
    best_route[:] = route[:]
    if not return_routes:
        print("------------------------------------------")
        print("  Method: 2-pass Metropolis")
        print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_path, np.int_(route))
    route_iter_best = np.zeros(n)
    route_iter_best[:] = best_route[:]
    count = 0
    new_route = np.zeros(n)
    count_last_iter = 0
    while count < max_iter:
        count += 1
        i = np.random.randint(n)
        j = np.random.randint(n)
        if i == j:
            continue
        new_route[:] = best_route[:]
        new_route[i] = best_route[j]
        new_route[j] = best_route[i]
        new_path = ComputeTotalDist(dist_data, new_route)
        if new_path < best_path:
            best_path = new_path
            best_route[:] = new_route[:]
            count_last_iter = count
    if not return_routes:
        print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    else:
        return best_path, best_route, count_last_iter


def ThreePassMetropolis(dist_data, route, max_iter, return_routes=False):
    n = len(route)
    best_route = np.zeros(n)
    best_path = ComputeTotalDist(dist_data, route)
    best_route[:] = route[:]
    if not return_routes:
        print("------------------------------------------")
        print("  Method: 3-pass Metropolis")
        print("------------------------------------------")
    # print("Starting path: %.2f \t" %best_path, np.int_(route))
    route_iter_best = np.zeros(n)
    route_iter_best[:] = best_route[:]
    count = 0
    new_route = np.zeros(n)
    while count < max_iter:
        count += 1
        i = np.random.randint(n)
        j = np.random.randint(n)
        k = np.random.randint(n)
        if i == j or j == k or i == k:
            continue
        new_route[:] = best_route[:]
        new_route[i] = best_route[j]
        new_route[j] = best_route[k]
        new_route[k] = best_route[i]
        new_path = ComputeTotalDist(dist_data, new_route)
        if new_path < best_path:
            best_path = new_path
            best_route[:] = new_route[:]
    if not return_routes:
        print("Better path:   %.2f \t" % best_path, np.int_(best_route))
    else:
        return best_path, best_route


def MetroRandInit(dist_data, route, two_or_three, max_iter, runs):
    best_route = np.zeros(len(route))
    best_path = ComputeTotalDist(dist_data, route)
    new_route = np.zeros(len(route))
    new_route[:] = route[:]
    count = 0
    print("------------------------------------------")
    print("  Method: %d-pass Metropolis rand. inits." % two_or_three)
    print("------------------------------------------")
    if two_or_three == 2:
        MetropolisFunction = TwoPassMetropolis
    elif two_or_three == 3:
        MetropolisFunction = ThreePassMetropolis
    while count < runs:
        count += 1
        np.random.shuffle(new_route)  # Create random starting route
        new_path, new_route, iterations = MetropolisFunction(
            dist_data, new_route, max_iter, True
        )
        if new_path < best_path:
            best_path = new_path
            best_route[:] = new_route[:]
            print(
                "Better path:   %.2f \t" % best_path,
                np.int_(best_route),
                "run:",
                count,
                ", iter:",
                iterations,
            )


def SimulatedAnnealing(dist_data, route, iterations):
    n = 24
    if len(route) < n:
        print("This works only with 24 cities. Exiting...")
        sys.exit(0)
    new_route, cur_route, best_route = np.zeros(n), np.zeros(n), np.zeros(n)
    new_route[:] = route[:]
    np.random.shuffle(new_route)
    cur_route[:] = new_route[:]
    best_route[:] = new_route[:]
    print("------------------------------------------------")
    print("  Method: Simulated Annealing, single rand.init.")
    print("  NB: Not finished")
    print("------------------------------------------------")
    print(
        "New start path: %.2f \t" % ComputeTotalDist(dist_data, new_route),
        np.int_(new_route),
    )
    from math import exp

    route_array_to_plot = []
    # p0 = 0.5
    # p1 = 0.01
    # path0 = 31500.0  # Average length of random 24-city path
    # path1 = 12000.0  # Maybe less than global optimum
    # T_init = -path0/np.log(p0)
    # T_end  = 0.01
    """
    e(-path0/T_init) = 0.5
    """
    # print(T_init,T_end)
    # p_const = path0/T_init
    cur_path = ComputeTotalDist(dist_data, new_route)
    best_path = cur_path
    for count in range(1, iterations + 1):
        i = np.random.randint(n)
        j = np.random.randint(n)
        if i == j:
            continue
        new_route[:] = cur_route[:]
        new_route[i] = cur_route[j]
        new_route[j] = cur_route[i]
        new_path = ComputeTotalDist(dist_data, new_route)
        if new_path < cur_path:
            cur_path = new_path
            cur_route[:] = new_route[:]
            route_array_to_plot.append(cur_path)
        else:
            T = 0.00856474 * exp(0.00012911 * new_path) / count ** (1.0 / 2)
            # p1 = exp(-new_path/float(p_const*T))
            p2 = np.random.random_sample()
            if T > p2:  # Accept bad move
                cur_path = new_path
                cur_route[:] = new_route[:]
                route_array_to_plot.append(cur_path)
                # print(T,p1,p2)
                # raw_input()
        if new_path < best_path:
            best_path = new_path
            best_route[:] = new_route[:]
            print(
                "Better path:   %.2f \t" % best_path,
                np.int_(best_route),
                "count:",
                count,
            )
    import matplotlib.pyplot as plt

    x = range(len(route_array_to_plot))
    plt.plot(x, route_array_to_plot)
    plt.show()


def MetroRandInitEvo(dist_data, route, max_iter, runs):
    n = 24
    if len(route) < n:
        print("This works only with 24 cities. Exiting...")
        sys.exit(0)
    best_route = np.zeros(len(route))
    best_route[:] = route[:]
    best_path = ComputeTotalDist(dist_data, route)
    total_best_path = 1e100
    new_route = np.zeros(len(route))
    new_route[:] = route[:]
    count = 0
    print("------------------------------------------")
    print("  Method: EVO Metropolis rand. inits.")
    print("  NB: NOT FINISHED")
    print("------------------------------------------")
    while count < runs:
        count += 1
        iterations = 0
        np.random.shuffle(best_route)  # Create random starting route
        while iterations < max_iter:
            print(iterations)
            rand_iter = np.random.randint(
                10, 150
            )  # Number of iterations with Two/Three pass
            iterations += rand_iter
            random_number = np.random.random_sample()
            new_route[:] = best_route[:]
            best_path = ComputeTotalDist(dist_data, best_route)
            if random_number < 0:
                new_path, new_route = TwoPassMetropolis(
                    dist_data, new_route, rand_iter, True
                )
            elif random_number < 0:
                new_path, new_route = ThreePassMetropolis(
                    dist_data, new_route, rand_iter, True
                )
            else:
                counter = 0
                while True:
                    counter += 1
                    cai = np.random.randint(n)  # Cut at index
                    hmis = 2  # np.random.randint(2,10) # How many in subset
                    """if (n - cai) < hmis: # Apparently numpy fixes this automatically
                        hmis = n - cai # Check if subset surpasses last element
                    if hmis == 1:
                        counter -= 1
                        continue # No change, continue to next iterations"""
                    new_route[:] = best_route[:]
                    subset = best_route[cai : cai + hmis + 1]
                    np.random.shuffle(subset)  # Shuffle subset
                    new_route[cai : cai + hmis + 1] = subset
                    new_path = ComputeTotalDist(dist_data, new_route)
                    if new_path < best_path or counter > rand_iter:
                        print(new_path)
                        break  # Iterate until we get a better path
            if new_path < best_path:
                # print(new_path,best_path)
                best_path = new_path
                best_route[:] = new_route[:]
                # print("Better path:   %.2f" %best_path, np.int_(best_route)
                # ,"run:",count)
        if best_path < total_best_path:
            print("Better path:   %.2f" % best_path, np.int_(best_route), "run:", count)
            total_best_path = best_path


def GeneticAlgo2Pass(dist_data, route, pool_size=20, generations=50, no_print=False):
    n = 24
    best_path = 1e100
    glob_opt_reached = False
    mutation_param = int(n / 2)
    mutation_list = np.zeros(pool_size)
    new_route = np.zeros(n)
    new_route[:] = route[:]
    if len(route) < n:
        print("This works only with 24 cities. Exiting...")
        sys.exit(0)
    pool = np.zeros((pool_size, n))
    pool_paths = np.zeros(pool_size)
    for i in range(pool_size):
        np.random.shuffle(route)
        pool[i, :] = route
        pool_paths[i] = ComputeTotalDist(dist_data, route)
    if not no_print:
        print("------------------------------------------")
        print("  Method: Genetic Algorithm")
        print("  Pool size: %d, generations < %d" % (pool_size, generations))
        print("------------------------------------------")
    for gen in range(generations):
        for current_route, i in zip(pool, range(pool_size)):
            new_route[:] = current_route[:]
            """ Mutate a subset of current_route"""
            cai = np.random.randint(n)  # Cut at index
            hmis = np.random.randint(3, mutation_param)  # How many in subset
            mutation_list[i] = hmis
            subset = new_route[cai : cai + hmis + 1]
            np.random.shuffle(subset)  # Shuffle subset
            new_route[cai : cai + hmis + 1] = subset
            # new_path = ComputeTotalDist(dist_data,new_route)
            """ Run 2 Pass until a local optimum (most likely) is reached """
            if False:  # i < pool_size/2:
                new_path, new_route, TPM_iter = TwoPassMetropolis(
                    dist_data, new_route, 3500, True
                )
            else:
                new_path, new_route, TPM_iter = HillClimber(
                    dist_data, new_route, 40, True
                )
            pool[i, :] = new_route
            pool_paths[i] = ComputeTotalDist(dist_data, new_route)
        i_best = np.argmin(pool_paths)
        new_route = pool[i_best, :]
        if pool_paths[i_best] < (best_path - 1e-5):
            best_path = pool_paths[i_best]
            if not no_print:
                print(
                    "Average path length %.2f" % np.mean(pool_paths),
                    ", best path %.2f" % (min(pool_paths)),
                    ", gen",
                    gen,
                    ", mut. param. of survivor:",
                    mutation_list[i_best],
                )
        if pool_paths[i_best] < 12287.07 + 1e-5:
            glob_opt_reached = True
            if not no_print:
                print("Global optimum reached for route:")
                print(np.int_(new_route))
            break
        for i in range(pool_size):
            pool[i, :] = new_route  # The only survivor until next iteration
    """ # """
    route = np.int_(range(n))  # Reset for another method
    return gen, glob_opt_reached


if __name__ == "__main__":
    dist_data, N = LoadData("european_cities.dat")
    if len(sys.argv) > 1:
        N_choice = int(sys.argv[1])
    else:
        N_choice = 24
    route = np.int_(range(N_choice))
    print("------------------------------------------")
    print("Starting path:  %.2f \t" % ComputeTotalDist(dist_data, route), route)

    # ---------------#
    # ### Methods ####
    # Uncomment the different solvers you want to use.   #
    # NB: Someone requires a specific length of the path #
    # ---------------#
    # BruteForceSearch(dist_data,route)
    # RandomSearch(dist_data,route,10000)
    # GreedySearch(dist_data,route)
    # HillClimber(dist_data,route,100)
    # HillClimberFromGreedy(dist_data,route,100)
    # TwoPassMetropolis(dist_data,route,3500)
    # ThreePassMetropolis(dist_data,route,3500)
    # HillClimberRandInit(dist_data,route,40,200)
    # MetroRandInit(dist_data,route,2,3500,400) # 2-pass
    # MetroRandInit(dist_data,route,3,3500,200) # 3-pass

    # MetroRandInitEvo(dist_data,route,1000,1)
    # SimulatedAnnealing(dist_data,route,20000)
    # HillClimberMaxSlow(dist_data,route,1000)

    pool_size = 20
    max_generations = 200
    print("Pool size, generations needed, found global optimum T/F")
    for i in range(10):
        gen, glob_opt_reached = GeneticAlgo2Pass(
            dist_data, route, pool_size, max_generations, no_print=True
        )
        print("%d, %.3d," % (pool_size, gen))


# ##########
# List of best solutions to 24 cities
# 12362.92 	[23  2 17 22 15 13 18  0 12  7 11 16  3  8  6 21 19 14 10  4  9 20  1  5]
# 12334.35 	[22  5  1 20  9  4 10 14 19 21  6 23  2  8  3 16 11  7 12  0 18 13 15 17]
# 12325.93 	[16  3  8  2  6 21 19 14 10  4  9 20  1  5 22 23 17 15 13 18  0 12  7 11]
# 12287.07 	[15 13 18  0 12  7 11 16  3  8  6 21 19 14 10  4  9 20  1  5 22 23  2 17]
#
# Pool size, generations needed
