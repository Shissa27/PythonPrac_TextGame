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
                    print("Вы смогли покинуть ваш кошмар ?")
                    break
                if(self.CurrentRoom.Flag == -1):
                    print("DEAD END \n Вам от сюда не выбратся")
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
info_list = [[["Пойти назад", 1],["Пойти вперёд ", 2 ],["Проверить сундук",3]],
             [],
             [["Двигаться вперёд", 6], ["Прыгунть в окно", 4]],
             [["Двигаться дальше", 4]],
              [["Выбрать правую дверь ", 7],["Выбрать левую дверь", 5]],
             [["Прыгнуть в люк", 3], ["Пойти дальше", 7]],
             [],
             [["Пойти в дверь от которой исходит свет", 5], ["Пойти вперед", 8],["Пойти в проход откуда веет сыростью",6], ["Уснуть", 9]],
             [["Идти вперёд", 9],["Повернуть в проход откуда веет сыростью",6]],
             []]

#сам список с комнатами, второй параметр - флаг,0 - комната, 1 - победа, -1 - луз
TestRooms = []
TestRooms.append(Room(info_list[0], 0))
TestRooms.append(Room(info_list[1], -1))
TestRooms.append(Room(info_list[2], 0))
TestRooms.append(Room(info_list[3], 0))
TestRooms.append(Room(info_list[4], 0))
TestRooms.append(Room(info_list[5], 0))
TestRooms.append(Room(info_list[6], -1))
TestRooms.append(Room(info_list[7], 0))
TestRooms.append(Room(info_list[8], 0))
TestRooms.append(Room(info_list[9], 1))
#присваиваются Id комнатам
for i in range(10):
    TestRooms[i].ID = i
TestRooms[0].info = "Вы оказались в темном коридоре  старого дома\n Кажется, что вы только что были в другом месте\n" \
                    "Вы всё ещё ощущаете тепло солнца на коже\n Но вспомнить, как оказались тут не получается \n" \
                    "Слева от вас находися старый сундук, но путь к нему кажется не прочным\n"

TestRooms[1].info = "Развернувшись вы идете назад\n" \
                    "Коридор кажется очень длинным, но в далеке виден свет. Вы решаете перейти на бег\n " \
                    "Через некторое время вы выбиватесь из сил. Вы понимате, что не сможете дойти до света и хотете вернуться\n" \
                    "Сколько вы бы не шли назад, вы не можете дойти до начала пути"

TestRooms[2].info = "Через некторое время вы доходите до окна, коридор даже не думает заканчиваться\n" \
                    "Вы открыли окно. От туда дует ветер, хотя видна только темнота"

TestRooms[3].info = "Вы падаете несколько секунд. После преземления вы оказваетесь в пустой комнате\n" \
                    "Перед вами массивная двреь. С трудом вы смогли открыть её"

TestRooms[4].info = "Вы долго двигатесь вперед по коридору\n" \
                    "Со временем вы начинаете чувствовать нарастающую тревогу и усталость\n" \
                    "Наконец вы доходите до комноты. Перед собой вы видите две двери\n" \
                    "На правой вы видите надпись \n {Выход} \n" \
                    "Из щелей между стеной и левой дверью вы видете теплый свет, так сильно отличающийся от бледного освещения коридоров"

TestRooms[5].info = "Вы окзались в теплой и светлой комнате\n" \
                    "В комнате есть камин" \
                    "Перед собой вы видите люк и проход длаьше\n" \
                    "С трудом вы смогли открыть люк, от туда пахнет сыростью\n" \
                    "В коридоре свет может осветить только несколько метров"

TestRooms[6].info = "Вы двигатесь по коридору\n" \
                    "Через пару часов в видите перед собой широкий коридор. Вы даже не видете боковых стен во тьме\n" \
                    "Пол коридора мокрый. Вы решаете продолжить путь\n" \
                    "Со временем вы замечаете, что пол уходит все становится глубже\n" \
                    "Когда вода доходит до колен, вы решаете развернутся\n" \
                    "Вы идёте назад, но пол также уходит в глубь вода\n" \
                    "Вскоре вам приходится начать плыть, а гладь воды покрывается небольшими волнами\n" \
                    "Спустя некотрое время вы уже не можете дотянутся до дна, а волны мешают плыть к выходу\n" \
                    "Силы уходят. Вы решаете их сохранить и пережить шторм в воде\n" \
                    "Несколько часов вы пытаетесь выжить среди огрымных воле\n" \
                    "Пока силы вас не покидают окнчательно\n" \
                    "Вы уходите под воду "

TestRooms[7].info = "Вы оказались на перекрестке\n Усталость стала сильнее. Вам приходится боротся со сном\n" \

TestRooms[8].info = "Вы долгое время двигатесь вперед, усталось становится всё сильнее \n" \
                    "Вы слышите голос предлагающий вам свернуть направо\n" \
                    "Вы думаете, что у вас галюцинации от усталости\n" \
                    "Вы быстро осознаете, что уже долгое время не видели никаких развилок\n" \
                    "Голос говорит, что это единственная возможность выбраться\n" \
                    "Что он ваш друг и ждёт вас там где вы были до кошмара\n " \
                    "Как только вы пытаетесь вспомнить его, появляется дверь\n" \
                    "Это ведь хороший знак?"
TestRooms[9].info = "Вы идёте вперед\n" \
                    "Сил нет\n" \
                    "Нужно поспать\n" \
                    "Как только вы закрыли глаза, вы видите тёплый свет\n" \
                    "Конец......"
game = GameDriver()
game.setRooms(TestRooms,10)
game.createMap()
game.findDeadEnds()
game.startGame()