#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright(C) 2020 YulKa (montypie)
# four different chars with stats

import matplotlib.pyplot as plt
import csv
import numpy as np

""" Pie charts of worldpop 2020 """

labels,numbers,sizes = [],[],[]
csv_reader = csv.reader(open('inputs/worldpop2020.csv'))
# "WorldPart","Pop","WorldPop","GrowthRate","PopDensity"

firstline = True
for line in csv_reader:
    if firstline:
        firstline = False
        continue
    labels.append(line[0])
    numbers.append(int(line[1]))
    sizes.append(float(line[2]))

d_numbers = []
for num in numbers:
    d_numbers.append('{}'.format(round(float(num/1000000), 2)))

colors = ['#ffb35f','#d95655','#a19fff', '#a0c0a0', '#cdff9f', '#5fabff']

plt.figure(figsize=plt.figaspect(1))

plt.pie(numbers, labels=d_numbers, colors=colors, startangle=65)
plt.title('2020 population by world parts, in millions')
plt.legend(labels)
plt.savefig("outputs/world_pie1.png")
plt.show()
