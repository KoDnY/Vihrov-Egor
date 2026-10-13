SIZE = get_world_size()

WOOD_COLS = [0, 1]
HAY_COLS = [2]
CARROT_COLS = [3]
PUMP_START = 4
BLOCK = 3


def zone(col, row):
	if col in WOOD_COLS:
		return "wood"
	if col in HAY_COLS:
		return "hay"
	if col in CARROT_COLS:
		return "carrot"
	if col >= PUMP_START and row < BLOCK:
		return "pumpkin"
	return "sunflower"


def plant_here(col, row):
	z = zone(col, row)
	if z == "wood":
		if (col + row) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
	elif z == "carrot":
		plant(Entities.Carrot)
	elif z == "pumpkin":
		plant(Entities.Pumpkin)
	elif z == "sunflower":
		plant(Entities.Sunflower)


def farm_cell(col, row):
	z = zone(col, row)

	if z == "hay":
		if can_harvest():
			harvest()
		return

	if get_ground_type() == Grounds.Grassland:
		till()

	if z == "pumpkin":
		e = get_entity_type()
		if e == None:
			plant(Entities.Pumpkin)
			return
		if e == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			return
		if can_harvest() and measure() > 1:
			if num_items(Items.Weird_Substance) < 1000:
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
			harvest()
			plant(Entities.Pumpkin)
		return

	if z == "carrot":
		if get_water() < 0.9 and num_items(Items.Water) > 0:
			use_item(Items.Water)
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		if can_harvest():
			harvest()
		plant(Entities.Carrot)
		return

	if z == "wood":
		if can_harvest():
			harvest()
		plant_here(col, row)
		return

	if can_harvest():
		harvest()
	plant(Entities.Sunflower)


def farm_world():
	for col in range(SIZE):
		for row in range(SIZE):
			farm_cell(col, row)
			move(North)
		move(East)


for col in range(SIZE):
	for row in range(SIZE):
		if zone(col, row) != "hay":
			if get_ground_type() == Grounds.Grassland:
				till()
		plant_here(col, row)
		move(North)
	move(East)

while True:
	farm_world()