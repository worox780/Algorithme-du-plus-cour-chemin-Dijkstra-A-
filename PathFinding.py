class PathFinding:
    def __init__(self, _size:tuple, _start_point:tuple, _end_point:tuple, _grid:list) -> None:
        self.size:tuple = _size
        self.start_point:tuple = _start_point
        self.end_point:tuple = _end_point
        self.grid_map:list = _grid
        self.point_now:int = 0

        self.lst_open_list:list = []
        self.lst_close_list:list = []

        self.close_lst_point:list = []
        self.close_lst_value:list = []
        self.close_lst_parent:list = []
        self.open_lst_point:list = []
        self.open_lst_value:list = []
        self.open_lst_parent:list = []

        self.close_lst_point.append(_start_point)
        self.close_lst_value.append(0)
        self.close_lst_parent.append(None)

        self.iteration_nb:int = 0

        self.all_point_visited:list = []
    
    def Reset(self):
        self.point_now:int = 0

        self.lst_open_list:list = []
        self.lst_close_list:list = []

        self.close_lst_point:list = []
        self.close_lst_value:list = []
        self.close_lst_parent:list = []
        self.open_lst_point:list = []
        self.open_lst_value:list = []
        self.open_lst_parent:list = []

        self.close_lst_point.append(self.start_point)
        self.close_lst_value.append(0)
        self.close_lst_parent.append(None)

        self.iteration_nb = 0
        self.all_point_visited = []

    def Get_Node_Connected_To_Current(self, map:list, point:tuple, cost:int) -> list:
        """
        Note
        Essayer de modifier les coefficients pour l'ajout des valeurs dans la liste "lst_inter".
        Cela donne des résulats très drôles ;).
        
        Indication
        Dans le cas actuelle (0,1) qui correspondent aux facteurs de la ligne 61, l'algorithme se comporte comme A*.
        Si les coefficients sont diposés ainsi (1,0), l'algorithme se comporte comme Dijkstra.
        """
        lst_inter = [] #liste de stockage intermédiaire
        lst_pos_temp = [(point[0],point[1]+1), (point[0],point[1]-1), (point[0]-1,point[1]), (point[0]+1,point[1])]
        for i in lst_pos_temp: #lecture de tous les noeuds connectés
            if (0 <= i[0]) and (i[0] < self.size[0]) and (0 <= i[1]) and (i[1] < self.size[1]) and map[i[1]][i[0]] in [-2, -1, 0]: #Vérification de si les noeuds ne sont pas hors de la liste
                lst_inter.append([i, 0.5*(cost+1) + 1*self.Distance_End_Point(i)]) #Ajout du noeud si tout est bon, avec ses coordonnées et son cout de transport direct
        return lst_inter

    def Distance_End_Point(self, _node:tuple) -> float:
        return (self.end_point[0]-_node[0])**2+(self.end_point[1]-_node[1])**2
    
    def Insertion(self, _value:int):
        a = 0
        b = len(self.open_lst_value) - 1
        if b < 0: return 0
        while True:
            if (a+b)%2 == 1:
                mid = (a+b+1)//2
            else:
                mid = (a+b)//2
            if (self.open_lst_value[a] == self.open_lst_value[b]) or (abs(a-b)-1 == 0):
                if self.open_lst_value[b] < _value: return b+1
                return b
            if self.open_lst_value[mid] > _value: b = mid
            else: a = mid

    def Check_End_Point(self, end_point, point):
        if (end_point == point): return [True, self.Get_Shortest_Path(), self.all_point_visited]
        return [False, False, self.all_point_visited]

    def Get_Shortest_Path(self):
        _point_now = self.point_now
        cost_path = self.close_lst_value[self.point_now]
        lst_chemin = []
        max_loop = 0
        while (self.close_lst_point[_point_now] != self.start_point and max_loop < 100):
            lst_chemin.append(self.close_lst_point[_point_now])
            _point_now = self.close_lst_point.index(self.close_lst_parent[_point_now])
            max_loop += 1
        lst_chemin.append(self.close_lst_point[_point_now])
        lst_chemin.reverse()
        lst_chemin.pop(-1)
        lst_chemin.pop(0)
        self.all_point_visited.remove(self.end_point)
        return lst_chemin, cost_path

    def Main(self) -> list:
        self.Reset()
        while True:
            inter_value = self.Get_Node_Connected_To_Current(self.grid_map, self.close_lst_point[self.point_now], self.close_lst_value[self.point_now])
            for i in inter_value:
                if i[0] in self.open_lst_point:
                    pos_inter = self.open_lst_point.index(i[0])
                    if self.open_lst_value[pos_inter] > i[1]: self.open_lst_value[pos_inter] = i[1]
                elif not i[0] in self.close_lst_point:
                    inter_value = self.Insertion(i[1])
                    self.open_lst_value.insert(inter_value, i[1])
                    self.open_lst_point.insert(inter_value, i[0])
                    self.open_lst_parent.insert(inter_value, self.close_lst_point[self.point_now])
                    self.all_point_visited.append(i[0])
            
            self.point_now = 0
            if len(self.open_lst_point) == 0: return (False, False, self.all_point_visited)
            self.close_lst_point.append(self.open_lst_point[self.point_now])
            self.close_lst_value.append(self.open_lst_value[self.point_now])
            self.close_lst_parent.append(self.open_lst_parent[self.point_now])
            self.open_lst_point.pop(self.point_now)
            self.open_lst_value.pop(self.point_now)
            self.open_lst_parent.pop(self.point_now)
            self.point_now = -1
            self.iteration_nb += 1
            inter_value_end_point = self.Check_End_Point(end_point=self.end_point, point=self.close_lst_point[-1])
            if inter_value_end_point[0] or self.iteration_nb > 10_000:
                inter_value = inter_value_end_point
                return inter_value