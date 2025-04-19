import PathFinding
# Example file showing a circle moving on screen
import pygame

class Window:
	def __init__(self, _screen_size:tuple=(1080, 720), _grid_size:tuple=(18, 12), _dim_tile:int=60, _map_pathfinding_coor:tuple=((-1,-1), (19+2,13+2))) -> None:
		pygame.init()
		self.screen_size:tuple = _screen_size
		self.screen = pygame.display.set_mode(self.screen_size) #initialisation des paramètres de la fenêtre
		pygame.display.set_caption('Algorithme du plus court chemin')
		
		self.running:bool = True #variable pour le fonctionnement du script
		self.clock = pygame.time.Clock()
		self.ips:int = 60

		self.rang_lst_path:int = 0
		self.can_process_display_path:bool = True #Fonction pour l'affichage des noeuds et chemins visités
		self.is_mouse_pressed:bool = False #Est ce qu'un bouton est pressé

		self.grid_size:tuple = _grid_size #Dimension de la grille
		self.size_tile:int = _dim_tile #Dimension d'une case

		self.grid_map:list = [] #Liste de la carte

		self.list_inter_path:list = [] #Liste contenant tous les noeuds du plus court chemin. Utiliser pour conserver temporairement les noeuds de la liste -> list_path, durant l'affichage des noeuds de la liste -> list_visited_node
		self.list_inter_visited_node:list = [] #Liste contenant tous les noeuds visités par l'algorithme. Incrémente la liste -> list_visited_node
		
		self.dijkstra_init = PathFinding.PathFinding(_size=self.grid_size, _start_point=(0,0), _end_point=(self.grid_size[0]-1,self.grid_size[1]-1), _grid=self.grid_map) #Class de l'algorithme de Dijkstra et A*

		self.background_color:tuple = (89,89,89)
		self.line_color:tuple = (200,200,200)
		
		self.map_pathfinding_coor:tuple = _map_pathfinding_coor
		self.camera_position:tuple = (0,0)
		#----Partie du code à améliorer-----
		self.start_point:tuple = ((0,0), (0,0)) #première indice, position du noeuds dans la grille d'affichage, second, position de la caméra à l'instant de l'initialisation.
		self.end_point:tuple = ((self.grid_size[0]-1,self.grid_size[1]-1), (0,0)) #première indice, position du noeuds dans la grille d'affichage, second, position de la caméra à l'instant de l'initialisation.

		self.node_unload:dict = {} #dictionnaire qui continent l'ensemble des noeuds non affichés. Les noeuds sont rangés par clés qui correspondent à leur position en y.
	
	#-----Fonction appelé uniquement au lancement-----
	def Initialisation(self) -> None:
		self.grid_map = Initialisation_Game.Building_Grid(_grid_size=self.grid_size)
		self.grid_map[0][0] = -1 #Initialisation du point de départ
		self.grid_map[self.grid_size[1]-1][self.grid_size[0]-1] = -2 #Initialisation du point d'arrivé
		print
		for i_0 in range(1, self.map_pathfinding_coor[1][1]-self.map_pathfinding_coor[0][1]-1):
			for i_1 in [0, self.map_pathfinding_coor[1][0]-self.map_pathfinding_coor[0][0]-1]:
				node_inter:tuple = (self.map_pathfinding_coor[0][0]+i_1, self.map_pathfinding_coor[0][1]+i_0)
				if self.Is_node_On_Screen(_node=node_inter):
					self.grid_map[node_inter[1]-self.camera_position[1]][node_inter[0]-self.camera_position[0]] = -5
				else:
					if not str(node_inter[1]) in self.node_unload:
						self.node_unload[str(node_inter[1])] = []
					self.node_unload[str(node_inter[1])].insert(Insertion(_list=self.node_unload[str(node_inter[1])], _value=node_inter[0]), (-5, node_inter[0]))
		for i_0 in [0, self.map_pathfinding_coor[1][1]-self.map_pathfinding_coor[0][1]-1]:
			for i_1 in range(self.map_pathfinding_coor[1][0]-self.map_pathfinding_coor[0][0]):
				node_inter:tuple = (self.map_pathfinding_coor[0][0]+i_1, self.map_pathfinding_coor[0][1]+i_0)
				if self.Is_node_On_Screen(_node=node_inter):
					self.grid_map[node_inter[1]-self.camera_position[1]][node_inter[0]-self.camera_position[0]] = -5
				else:
					if not str(node_inter[1]) in self.node_unload:
						self.node_unload[str(node_inter[1])] = []
					self.node_unload[str(node_inter[1])].insert(Insertion(_list=self.node_unload[str(node_inter[1])], _value=node_inter[0]), (-5, node_inter[0]))
		print(self.node_unload)
	
	def Show_Grid(self) -> None:
		for i in self.grid_map: print(i)

	def Main(self) -> None:
		self.Initialisation()
		self.Display_Grid()
		pygame.display.update()
		while self.running:
			self.clock.tick(self.ips) #Mise à jour du rafraichissement de l'écran
			for event in pygame.event.get():
				self.Event_Controler(_event=event)
				self.Quit_Game(event)

	def Display_Searching(self) -> None:
		for i in self.list_inter_visited_node:
			inter_node = i
			if self.Is_node_On_Screen(_node=(inter_node[0]+self.map_pathfinding_coor[0][0], inter_node[1]+self.map_pathfinding_coor[0][1])):
				self.grid_map[inter_node[1]-(self.camera_position[1]-self.map_pathfinding_coor[0][1])][inter_node[0]-(self.camera_position[0]-self.map_pathfinding_coor[0][0])] = -4
			else:
				if not str(inter_node[1]+self.map_pathfinding_coor[0][1]) in self.node_unload:
					self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])] = []
				self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])].insert(Insertion(_list=self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])], _value=inter_node[0]+self.map_pathfinding_coor[0][0]), (-4, self.map_pathfinding_coor[0][0]+inter_node[0]))
		for i in self.list_inter_path:
			inter_node = i
			if self.Is_node_On_Screen(_node=(inter_node[0]+self.map_pathfinding_coor[0][0], inter_node[1]+self.map_pathfinding_coor[0][1])):
				self.grid_map[inter_node[1]-(self.camera_position[1]-self.map_pathfinding_coor[0][1])][inter_node[0]-(self.camera_position[0]-self.map_pathfinding_coor[0][0])] = -3
			else:
				if not str(inter_node[1]+self.map_pathfinding_coor[0][1]) in self.node_unload:
					self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])] = []
				value_inter_pos_node = Is_Value_In_List_Order(_list=self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])], _value=inter_node[0]+self.map_pathfinding_coor[0][0])
				if value_inter_pos_node[0]:
					self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])][value_inter_pos_node[1]] = (-3, inter_node[0]+self.map_pathfinding_coor[0][0])
				self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])].insert(Insertion(_list=self.node_unload[str(inter_node[1]+self.map_pathfinding_coor[0][1])], _value=inter_node[0]+self.map_pathfinding_coor[0][0]), (-3, self.map_pathfinding_coor[0][0]+inter_node[0]))
		self.Display_Grid()
		pygame.display.update()

	def Display_Grid(self) -> None:
		color_dict:dict = {
			"-5":(39,179,148),
			"-4":(163, 163, 163),
			"-3":(0,0,0),
			"-2":(0,0,255),
			"-1":(0,255,0),
			"1":(255,255,255)
		}
		self.screen.fill(self.background_color)
		#-----Affichage du cadrillage-----
		for i in range(self.grid_size[0]+1): #Affichage des collones
			pygame.draw.line(self.screen, pygame.Color(self.line_color), (i*self.size_tile,0), (i*self.size_tile, self.size_tile*self.grid_size[1]), 5)
		for i in range(self.grid_size[1]+1): #Affichage des lignes
			pygame.draw.line(self.screen, pygame.Color(self.line_color), (0,i*self.size_tile), (self.size_tile*self.grid_size[0], i*self.size_tile), 5)
		#-----Affichage des cases importantes-----
		for i in range(self.grid_size[1]):
			for ii in range(self.grid_size[0]):
				if self.grid_map[i][ii] != 0:
					self.screen.fill(color_dict[str(self.grid_map[i][ii])], rect = (ii*self.size_tile+4, i*self.size_tile+4, self.size_tile-7, self.size_tile-7))

	def Event_Controler(self, _event:pygame.event.Event) -> None:
		if _event.type == pygame.KEYDOWN:
			if _event.key == 115: self.Start_Searching() #Appuyer sur la touche -> S
			if _event.key == 99: #Appuyer sur la touche -> C
				self.Clear()
				self.can_process_display_path = False
			if _event.key == 112: self.can_process_display_path = not self.can_process_display_path #Appuyer sur la touche -> P
			if _event.key == 97: #Appuyer sur la touche -> A
				inter_input = int(input("speed_display")) #Récupération du taux de rafraichissement
				if inter_input >= 1: self.ips = inter_input #Mise à jour de la variable du taux de rafraichissement
			if _event.key in [1073741903, 1073741904, 1073741905, 1073741906]: #Droite->Gauche->Bas->Haut
				self.Mouving_Camera(_key=_event.key-1073741903)
		self.Input_Mouse_Block()

	def Start_Searching(self) -> None:
		self.Clear()
		self.dijkstra_init.size = (self.map_pathfinding_coor[1][0]-self.map_pathfinding_coor[0][0], self.map_pathfinding_coor[1][1]-self.map_pathfinding_coor[0][1])
		self.dijkstra_init.grid_map = self.Generate_Map_For_PathFinding(_min_value=self.map_pathfinding_coor[0], _max_value=self.map_pathfinding_coor[1])
		self.dijkstra_init.start_point = (self.start_point[0][0]-self.map_pathfinding_coor[0][0], self.start_point[0][1]-self.map_pathfinding_coor[0][1])
		self.dijkstra_init.end_point = (self.end_point[0][0]-self.map_pathfinding_coor[0][0], self.end_point[0][1]-self.map_pathfinding_coor[0][1])
		inter:list = self.dijkstra_init.Main()
		self.list_inter_visited_node = inter[2]
		self.list_inter_path = []
		self.can_process_display_path = True
		if inter[0] != False:
			self.list_inter_path = inter[1][0]
		self.Display_Searching()
	
	#-----Fonction pour le nétoyage des cases de recherches sur l'écran-----
	def Clear(self) -> None:
		self.can_process_display_path = False
		#-----Suppression des noeuds chargés-----
		for i in range(len(self.grid_map)):
			for ii in range(len(self.grid_map[i])):
				if self.grid_map[i][ii] in [-4,-3]: self.grid_map[i][ii] = 0
		#-----Suppression des noeuds non chargés-----
		for i_0 in self.node_unload:
			pop_inter = 0
			for i_1 in range(len(self.node_unload[i_0])):
				if self.node_unload[i_0][i_1-pop_inter][0] in [-4,-3]:
					self.node_unload[i_0].pop(i_1-pop_inter) #suppression des noeuds déchargés qui montrent les noeuds observés par l'algorithme
					pop_inter += 1
		self.Display_Grid()
		self.rang_lst_path = 0
		pygame.display.update()

	def Input_Mouse_Block(self) -> None:
		if pygame.mouse.get_pressed() != (False,False,False) and not self.is_mouse_pressed:
			self.is_mouse_pressed = True
			mouse_pos = (pygame.mouse.get_pos()[0]//self.size_tile, pygame.mouse.get_pos()[1]//self.size_tile)
			if pygame.mouse.get_pressed()[0]: #Clique gauche
				result:tuple = Mouse_Input.Left_Click(_mouse_pos=mouse_pos, _grid_map=self.grid_map)
				if result[0]:
					self.grid_map[result[1][1]][result[1][0]] = result[2]
					self.Display_Grid()
					pygame.display.update()
				elif result[1] == -2:
					self.Clear()
					self.grid_map[result[2][1]][result[2][0]] = 1
					self.Display_Grid()
					pygame.display.update()
			elif pygame.mouse.get_pressed()[1]: #Clique molette
				result:tuple = Mouse_Input.Click_Start_End(_mouse_pos=mouse_pos, _grid_map=self.grid_map)
				if result[0]:
					if self.Is_node_On_Screen(_node=self.start_point[0]):
						self.grid_map[self.start_point[0][1]+(self.start_point[1][1]-self.camera_position[1])][self.start_point[0][0]+(self.start_point[1][0]-self.camera_position[0])] = 0
					else:
						self.node_unload[str(self.start_point[0][1]+self.start_point[1][1])].remove((-1, self.start_point[0][0]+self.start_point[1][0]))
						if len(self.node_unload[str(self.start_point[0][1])]) == 0: self.node_unload.pop(str(self.start_point[0][1]), None)
					self.start_point = (result[1], self.camera_position)
					self.grid_map[result[1][1]][result[1][0]] = -1
					self.Display_Grid()
					pygame.display.update()
			elif pygame.mouse.get_pressed()[2]: #Clique droit
				result:tuple = Mouse_Input.Click_Start_End(_mouse_pos=mouse_pos, _grid_map=self.grid_map)
				if result[0]:
					if self.Is_node_On_Screen(_node=self.end_point[0]):
						self.grid_map[self.end_point[0][1]+(self.end_point[1][1]-self.camera_position[1])][self.end_point[0][0]+(self.end_point[1][0]-self.camera_position[0])] = 0
					else:
						self.node_unload[str(self.end_point[0][1]+self.end_point[1][1])].remove((-2, self.end_point[0][0]+self.end_point[1][0]))
						if len(self.node_unload[str(self.end_point[0][1])]) == 0: self.node_unload.pop(str(self.end_point[0][1]), None)
					self.end_point = (result[1], self.camera_position)
					self.grid_map[result[1][1]][result[1][0]] = -2
					self.Display_Grid()
					pygame.display.update()
		if pygame.mouse.get_pressed() == (False,False,False): self.is_mouse_pressed = False
	
	def Is_node_On_Screen(self, _node:tuple) -> bool:
		if _node[0] >= self.camera_position[0] and _node[0] <= self.camera_position[0]+self.grid_size[0]-1 and _node[1] >= self.camera_position[1] and _node[1] <= self.camera_position[1]+self.grid_size[1]-1:
			return True
		return False

	def Quit_Game(self, event) -> None:
		if event.type == pygame.QUIT:
			self.running = False
			self.Show_Grid()
			print("quit")
			pygame.quit()
	
	def Update_Size_Tile(self) -> int:
		return self.size_tile*self.screen_size[1]//720

	def Check_Modif_Screen_Size(self) -> None:
		if self.screen_size != (pygame.display.Info().current_w, pygame.display.Info().current_h):
			self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
			self.size_tile = self.Update_Size_Tile()
			self.Display_Grid()
			pygame.display.update()
	
	def Mouving_Camera(self, _key:int=1073741903) -> None:
		vector_dir:tuple
		if _key == 0: vector_dir = (-1,0)
		elif _key == 1: vector_dir = (1,0)
		elif _key == 2: vector_dir = (0,-1)
		else: vector_dir = (0,1)
		self.camera_position = (self.camera_position[0]+vector_dir[0], self.camera_position[1]+vector_dir[1])
		new_data:list = self.Load_Tile(_vector_dir=vector_dir)
		self.Unload_Tile(vector_dir)
		self.grid_map = self.Update_Map(vector_dir, new_data)
		self.Display_Grid()
		pygame.display.update()
	
	def Unload_Tile(self, _vector_dir:tuple) -> None:
		lst_grid:list = self.grid_map.copy()
		lst_value_inter:list = []
		if _vector_dir[1] < 0:
			lst_value_inter.append([self.camera_position[1]+self.grid_size[1]])
			lst_value_inter[0].append([])
			for i in range(self.grid_size[0]):
				if lst_grid[-1][i] != 0:
					lst_value_inter[0][1].append((lst_grid[-1][i], i+self.camera_position[0]))
		elif _vector_dir[1] > 0:
			lst_value_inter.append([self.camera_position[1]-1])
			lst_value_inter[0].append([])
			for i in range(self.grid_size[0]):
				if lst_grid[0][i] != 0:
					lst_value_inter[0][1].append((lst_grid[0][i], i+self.camera_position[0]))
		if _vector_dir[0] < 0:
			for i in range(self.grid_size[1]):
				if lst_grid[i][-1] != 0:
					lst_value_inter.append((self.camera_position[1]+i, [(lst_grid[i][-1], self.camera_position[0]+self.grid_size[0])]))
		elif _vector_dir[0] > 0:
			for i in range(self.grid_size[1]):
				if lst_grid[i][0] != 0:
					lst_value_inter.append((self.camera_position[1]+i, [(lst_grid[i][0], self.camera_position[0]-1)]))
		self.Register_Data_Tile(_data=lst_value_inter)
	
	def Load_Tile(self, _vector_dir:tuple) -> list:
		inter_value:list = []
		if _vector_dir[1] < 0:
			if str(self.camera_position[1]) in self.node_unload:
				inter_value = self.Select_Value_Unload(_list_value=self.node_unload[str(self.camera_position[1])].copy(), _start=self.camera_position[0], _end=self.camera_position[0]+self.grid_size[0]-1, _value_y=self.camera_position[1])
				self.node_unload[str(self.camera_position[1])] = inter_value[0]
				if len(self.node_unload[str(self.camera_position[1])]) == 0: self.node_unload.pop(str(self.camera_position[1]), None)
				return inter_value[1]
		elif _vector_dir[1] > 0:
			if str(self.camera_position[1]+self.grid_size[1]-1) in self.node_unload:
				inter_value = self.Select_Value_Unload(_list_value=self.node_unload[str(self.camera_position[1]+self.grid_size[1]-1)].copy(), _start=self.camera_position[0], _end=self.camera_position[0]+self.grid_size[0]-1, _value_y=self.camera_position[1])
				self.node_unload[str(self.camera_position[1]+self.grid_size[1]-1)] = inter_value[0]
				if len(self.node_unload[str(self.camera_position[1]+self.grid_size[1]-1)]) == 0: self.node_unload.pop(str(self.camera_position[1]+self.grid_size[1]-1), None)
				return inter_value[1]
		if _vector_dir[0] < 0:
			for i in range(self.grid_size[1]):
				if str(self.camera_position[1]+i) in self.node_unload:
					for ii in range(len(self.node_unload[str(self.camera_position[1]+i)])):
						if self.node_unload[str(self.camera_position[1]+i)][ii][1] == self.camera_position[0]:
							inter_value.append((i, self.node_unload[str(self.camera_position[1]+i)][ii][0], self.node_unload[str(self.camera_position[1]+i)][ii][1]-self.camera_position[0]))
							self.node_unload[str(self.camera_position[1]+i)].pop(ii)
							if len(self.node_unload[str(self.camera_position[1]+i)]) == 0: self.node_unload.pop(str(self.camera_position[1]+i), None)
							break
			return inter_value
		
		elif _vector_dir[0] > 0:
			for i in range(self.grid_size[1]):
				if str(self.camera_position[1]+i) in self.node_unload:
					for ii in range(len(self.node_unload[str(self.camera_position[1]+i)])):
						if self.node_unload[str(self.camera_position[1]+i)][ii][1] == self.camera_position[0]+self.grid_size[0]-1:
							inter_value.append((i, self.node_unload[str(self.camera_position[1]+i)][ii][0], self.node_unload[str(self.camera_position[1]+i)][ii][1]-self.camera_position[0]))
							self.node_unload[str(self.camera_position[1]+i)].pop(ii)
							if len(self.node_unload[str(self.camera_position[1]+i)]) == 0: self.node_unload.pop(str(self.camera_position[1]+i), None)
							break
			return inter_value
		return []
	
	def Select_Value_Unload(self, _list_value:list, _start:int, _end:int, _value_y:int) -> tuple:
		inter_value:list = []
		inter_pop:int = 0
		for i in range(len(_list_value)):
			if _list_value[i-inter_pop][1] <= _end and _list_value[i-inter_pop][1] >= _start:
				inter_value.append((_list_value[i-inter_pop][0], _list_value[i-inter_pop][1]-(self.camera_position[0])))
				_list_value.pop(i-inter_pop)
				inter_pop += 1
		return (_list_value, inter_value)

	def Update_Map(self, _vector_dir:tuple, _data:list) -> list:
		lst_grid:list = self.grid_map.copy()
		if _vector_dir[1] < 0:
			lst_grid.insert(0, [0 for i in range(self.grid_size[0])])
			lst_grid.pop(-1)
			for i in _data: lst_grid[0][i[1]] = i[0]
		elif _vector_dir[1] > 0:
			lst_grid.pop(0)
			lst_grid.insert(self.grid_size[1], [0 for i in range(self.grid_size[0])])
			for i in _data: lst_grid[self.grid_size[1]-1][i[1]] = i[0]
		
		if _vector_dir[0] < 0:
			for i in range(self.grid_size[1]):
				lst_grid[i].insert(0, 0)
				lst_grid[i].pop(-1)
			for i in _data: lst_grid[i[0]][i[2]] = i[1]
		elif _vector_dir[0] > 0:
			for i in range(self.grid_size[1]):
				lst_grid[i].insert(self.grid_size[0], 0)
				lst_grid[i].pop(0)
			for i in _data: lst_grid[i[0]][i[2]] = i[1]

		return lst_grid

	def Register_Data_Tile(self, _data:list):
		for i in _data:
			if len(i[1]) > 0:
				if str(i[0]) in self.node_unload:
					for ii in i[1]:
						index_insert = Insertion(_list=self.node_unload[str(i[0])], _value=ii[1])
						self.node_unload[str(i[0])].insert(index_insert,ii)
				else:
					self.node_unload[str(i[0])] = []
					for ii in i[1]:
						index_insert = Insertion(_list=self.node_unload[str(i[0])], _value=ii[1])
						self.node_unload[str(i[0])].insert(index_insert,ii)
	
	def Generate_Map_For_PathFinding(self, _min_value:tuple, _max_value:tuple) -> list:
		inter_grid_map:list = []
		for i in range(abs(_max_value[1]-_min_value[1])):
			inter_grid_map.append([0 for ii in range(abs(_max_value[0]-_min_value[0]))])
		size_creen_x_map_path:int = min(self.grid_size[0], max(0, (_max_value[0]-_min_value[0])-max(0, self.camera_position[0]-_min_value[0])-max(0, _max_value[0]-(self.camera_position[0]+self.grid_size[0]))))
		for i in range(_min_value[1], _max_value[1]):
			if str(i) in self.node_unload:
				for ii in self.node_unload[str(i)]:
					if _min_value[0] <= ii[1] and _max_value[0] >= ii[1]:
						inter_grid_map[i-_min_value[1]][ii[1]-_min_value[0]] = ii[0]
			if self.camera_position[1] <= i and self.camera_position[1]+self.grid_size[1]-1 >= i:
				for ii in range(size_creen_x_map_path):
					inter_grid_map[i-_min_value[1]][ii+(self.camera_position[0]-_min_value[0])] = self.grid_map[i-self.camera_position[1]][ii]
		return inter_grid_map



class Mouse_Input:
	def Left_Click(_mouse_pos:tuple, _grid_map:list) -> tuple:
		if _grid_map[_mouse_pos[1]][_mouse_pos[0]] == 1:
			return (True, _mouse_pos, 0)
		if _grid_map[_mouse_pos[1]][_mouse_pos[0]] == 0:
			return (True, _mouse_pos, 1)
		if _grid_map[_mouse_pos[1]][_mouse_pos[0]] in [-4,-3]: return (False, -2, _mouse_pos)
		return (False, -1)
	def Click_Start_End(_mouse_pos:tuple, _grid_map:list) -> tuple:
		if _grid_map[_mouse_pos[1]][_mouse_pos[0]] == 0:
			return (True, (_mouse_pos[0], _mouse_pos[1]))
		return (False, -1)

class Initialisation_Game():
	#-----Fonction permettant la fabrication de la grille d'affichage-----
	def Building_Grid(_grid_size:tuple) -> list:
		inter_list:list = []
		for i in range(_grid_size[1]):
			inter_list.append([0 for i in range(_grid_size[0])])
		return inter_list

def Insertion(_list:list, _value:int) -> int:
	a:int = 0
	b:int = len(_list) - 1
	mid:int
	if b < 0: return 0
	while True:
		if (a+b)%2 == 1:
			mid = (a+b+1)//2
		else:
			mid = (a+b)//2
		if (_list[a][1] == _list[b][1]) or (abs(a-b)-1 == 0):
			if _list[b][1] < _value: return b+1
			if _list[a][1] > _value: return a
			return b
		if _list[mid][1] > _value: b = mid
		else: a = mid

def Is_Value_In_List_Order(_list:list, _value:int) -> int:
	a:int = 0
	b:int = len(_list) - 1
	mid:int
	if b < 0: return (False, -1)
	while True:
		if (a+b)%2 == 1:
			mid = (a+b+1)//2
		else:
			mid = (a+b)//2
		if (_list[a][1] == _list[b][1]) or (abs(a-b)-1 == 0):
			if _list[b][1] == _value: return (True, b)
			elif _list[a][1] == _value: return (True, a)
			return (False,-1)
		if _list[mid][1] > _value: b = mid
		else: a = mid

start = Window().Main()
