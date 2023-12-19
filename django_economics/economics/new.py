
import numpy as np
from matplotlib import pyplot as plt

length = 10
fnx = lambda : np.random.randint(5, 50, length)
x = np.arange(length)
y1, y2, y3 = fnx(), fnx(), fnx()
areaLabels=['area1','area2','area3']
fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, y3)

loc = y1.argmax()
ax.text(loc, y1[loc]*0.25, areaLabels[0])

loc = y2.argmax()
ax.text(loc, y1[loc] + y2[loc]*0.33, areaLabels[1])

loc = y3.argmax()
ax.text(loc, y1[loc] + y2[loc] + y3[loc]*0.75, areaLabels[2]) 

plt.show()

print(loc, y1[loc] + y2[loc] + y3[loc]*0.75)