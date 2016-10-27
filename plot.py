import math
import re
import squarify

#values = []
#labels = []
pos2values = {}
pos2labels = {}
total_count = 0
with open('spanish_in_texas.out') as infile:
  for line in infile:
    if ' ' in line:
      parts = re.split(r'\s+', line)
      pos = parts[1]
      if int(parts[2]) > 100:
        if not pos2values.has_key(pos):
          pos2values[pos] = []
          pos2labels[pos] = []
        pos2values[pos].append(int(parts[2]))
        pos2labels[pos].append(parts[0])
        total_count += int(parts[2])

print """<style>
body { font-family: sans-serif; }
.rect { position: absolute; border: 1px black solid; font-size: 8pt; }
</style>"""

x_so_far = 0
#y_so_far = 0
for pos in sorted(pos2values.keys(), key=lambda pos: -sum(pos2values[pos])):
  values = pos2values[pos]
  labels = pos2labels[pos]

  #x = 0.
  #y = y_so_far
  x = x_so_far
  y = 0
  #width = 1000.
  #width = math.ceil(sum(values) / 1000.0)
  width = math.ceil(sum(values) * 1000.0 / total_count)
  height = 1000.
  #height = math.ceil(sum(values) / 1000.0)
  #y_so_far += height
  x_so_far += width
  values.reverse()
  labels.reverse()
  #values.append((width * height) - sum(values))
  #values.sort(reverse=True)

  rects = squarify.squarify(values, x, y, width, height)

  for rect, label in zip(rects, labels):
    print "<div class='rect' style='left: %dpx; top: %dpx; width: %dpx; height: %dpx;'>%s</div>" % (rect['x'], rect['y'], rect['dx'], rect['dy'], label)
