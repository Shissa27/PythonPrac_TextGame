from collections import deque

import graphviz
class GameDriver:
    Rooms = []
    Size = 0
    CurrentRoom = None


    def setRooms(self,rooms,size):
        self.Rooms = rooms
        self.Size = size


    def startGame(self):
        while(True):
            self.CurrentRoom = self.findById(0)

            while(True):
                self.CurrentRoom.showInfo()
                if( self.CurrentRoom.Flag == 1 ):
                    print("Победа!!!")
                    break
                if(self.CurrentRoom.Flag == -1):
                    print("Поражение X( ")
                    break
                self.CurrentRoom.showPaths()
                print('\n',"Введите номер варианта который вы хотите выборать")
                choosen = int(input())
                self.CurrentRoom = self.findById(self.CurrentRoom.Paths[choosen][1])
            print("Введите 0 чтобы закончить или любое другое число чтобы перезапустить ")
            if(int(input()) == 0):
                break
            else:
                continue


    def findById(self,id):
        return self.Rooms[id]


    def createMap(self):
        mapRooms = graphviz.Digraph(comment='MAP')
        for i in range(self.Size):
            mapRooms.node(str(i))
        pathList = []
        for room in self.Rooms:
            for path in room.Paths:
                pathList.append(str(room.ID)+str(path[1]))
        mapRooms.edges(pathList)
        print(mapRooms.source)


    def formMatrix(self):
        room_list = []
        paths_list = []
        for room in self.Rooms:
            paths = []
            for path in room.Paths:
                paths.append(path[1])
            room_list.append(room.ID)
            paths_list.append(paths)
        Matrix = dict(zip(room_list, paths_list))
        return Matrix

    def bfs(self, graph, start, end):
        visited = set()
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex == end:
                return True
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(graph[vertex])
        return False

    def findUnreachableVertices(self,graph, end):
        unreachable = []
        for vertex in graph.keys():
            if not self.bfs(graph, vertex, end):
                unreachable.append(vertex)
        return unreachable

    def findDeadEnds(self):
        for room in self.Rooms:
            if(room.Flag == 1):
                key = self.Rooms.index(room)
        print(key)
        Matrix = self.formMatrix()
        print(self.findUnreachableVertices(Matrix,key))


class Room:
    Paths = []
    Flag = 0
    info = ''
    ID = 0
    def __init__(self, paths,flag):
        self.Paths = paths
        self.Flag = flag
    def showPaths(self):
        i = 0
        for path in self.Paths:
            print(i,"   ",path[0],'\n')
            i += 1
    def showInfo(self):
        print(self.info)

#Тут создается список - комнат с путями, где путь список со строкой и направлением на комнату
info_list = [[["Вперёд", 1],["Направо ", 2 ]],
             [["Назад ",0],["Направо",3],["Налево",2],["ОЧчень вперёд",5]],
             [["Go",5]],
             [["Назад",2],["Вперёд",4]],
              [],
             []]
#сам список с комнатами, второй параметр - флаг,0 - комната, 1 - победа, -1 - луз
TestRooms = []
TestRooms.append(Room(info_list[0],0))
TestRooms.append(Room(info_list[1],0))
TestRooms.append(Room(info_list[2],0))
TestRooms.append(Room(info_list[3],0))
TestRooms.append(Room(info_list[4],1))
TestRooms.append(Room(info_list[5],-1))
#присваиваются Id комнатам
for i in range(6):
    TestRooms[i].info = "Room #" + str(i)
    TestRooms[i].ID = i
game = GameDriver()
game.setRooms(TestRooms,6)
game.createMap()
game.findDeadEnds()
game.startGame()