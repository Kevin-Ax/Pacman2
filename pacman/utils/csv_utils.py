from csv import reader


def import_csv_layout(path: str):
  terrain = []
  with open(path) as map:
    layout = reader(map, delimiter=',')
    for row in layout:
      terrain.append(list(row))
  return terrain
