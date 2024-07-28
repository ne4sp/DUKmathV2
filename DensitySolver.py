import numpy as np
from parsing import get_lines, LightValues, rms
import matplotlib.pyplot as plt
class Measure:
    levels = [] # 'input levels'
    intersections_train = [[], # intersections
                           []] # 'densities'
    intersections_new = [] # 'intersections'
    near_right_args = [] # 'closest point near the crosses between input and etalon line from right'
    near_left_args = [] # 'closest point near the crosses between input and etalon line from left'
    result_value = float # conc
    result_error = float # rsm of conc

    # def levels_normalize(self):
    #     minLevel = min(self.levels)
    #     maxLevel = max(self.levels)
    #     lenLevel = maxLevel - minLevel
    #     minLevel += lenLevel * 0.35
    #     maxLevel -= lenLevel * 0.05
    #     lenLevel = maxLevel - minLevel
    #     levelStep = lenLevel / (len(self.levels)-1)
    #     levels = [minLevel + i*levelStep for i in range(len(self.levels))]
    #     self.levels = levels

    def ox(self, lines):
        levels = self.levels
        group = []
        if type(lines) == LightValues:
            for level in levels:
                intersection = [(((level - lines.lv[i]) * ((i + 1) - i)) / (lines.lv[i + 1] - lines.lv[i])) + i for i
                                in range(len(lines.lv) - 1) if lines.lv[i] <= level <= lines.lv[i + 1]]
                group.append(intersection[0])
            self.intersections_new = np.array(group)
            return
        for level in levels:
            arr1 = []
            arr2 = []
            for line in lines:
                intersection = [(((level-line.lv[i])*((i+1)-i))/(line.lv[i+1]-line.lv[i])) + i for i
                                in range(len(line.lv)-1) if line.lv[i] <= level <= line.lv[i+1]]
                density = [line.rv for i in range(len(line.lv)-1) if line.lv[i] <= level <= line.lv[i+1]]
                arr1.append(intersection[0])
                arr2.append(density[0])
            group.append([arr1, arr2])
        self.intersections_train = np.array(group)
        return

    def near_points(self):
        intersections_new = self.intersections_new
        intersections_train = self.intersections_train
        near_left_args = []
        near_right_args = []
        for i in range(len(intersections_new)):
            near_left = [[intersections_train[i][0][j], intersections_train[i][1][j]] for j in range(len(intersections_train[i][0])) if intersections_train[i][0][j] < intersections_new[i]]
            near_left_args.append(near_left[0])
        for i in range(len(intersections_new)):
            near_right = [[intersections_train[i][0][j], intersections_train[i][1][j]] for j in range(len(intersections_train[i][0])) if intersections_train[i][0][j] > intersections_new[i]]
            near_right_args.append(near_right[0])
        self.near_right_args = near_right_args
        self.near_left_args = near_left_args

    def calculate(self):
        result_list = []
        for i in range(len(self.levels)):
            l_front = self.near_left_args[i][0]
            r_front = self.near_right_args[i][0]
            l_density = self.near_left_args[i][1]
            r_density = self.near_right_args[i][1]
            density = l_density + (r_density - l_density) * abs(self.intersections_new[i] - l_front) / abs(r_front - l_front)
            result_list.append(density)
        self.result_value = sum(result_list) / len(result_list)
        self.result_error = rms(result_list, self.result_value)




measure = Measure()
measure.levels = [3500]
# measure.levels_normalize()
lines = get_lines('plotviewing/trlog.txt')
measure.ox(lines)
# [plt.plot(level[0], level[1]) for level in measure.intersections_train]
print(measure.intersections_train[0][0][0])
plt.plot([measure.intersections_train[0][0][0], measure.intersections_train[0][0][-1]], [lines[0].rv, lines[-1].rv])
plt.plot(measure.intersections_train[0][0], measure.intersections_train[0][1])
plt.show()
# plt.plot(measure.intersections_train)
# plt.show()
# lines = get_lines('conc_history (2).log')
# measure.ox(lines[1])
# measure.near_points()
# measure.calculate()
# print(measure.result_value, ' ', measure.result_error)