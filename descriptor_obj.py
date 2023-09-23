from graphicsitem import *
#para cada objeto no display file
#tomando seu nome, seu tipo, seus vértices e suas arestas.
#Chame o descritor para cada objeto de seu mundo.
class FileObj:
    def __init__(self):
        pass

    def open_file(self, file):
        dic = {}
        dic["name"] = ""
        dic["vertices"] = ""
        vertices = []
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        if parts[0] == 'g':
                            name = parts[1]
                    if len(parts) == 4 and parts[0] == 'v':
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        vertices.append([x, y, z])
                dic["name"] = name
                dic["vertices"] = vertices
        except Exception as e:
            print(f"Error reading the file: {e}")
        return dic

    def save_file(self, display_file: list, file_name: str):
        objects = []
        try:
            with open(file_name, 'w+') as file:
                for obj in display_file:
                    dic = {}
                    lista = []
                    if isinstance(obj, Reta):
                        lista.append(obj.line().x1(), obj.line.y1(), 1.0)
                        lista.append(obj.line().x2(), obj.line.y2(), 1.0)
                        dic["vertices"] = lista
                        dic["name"] = obj.name
                        objects.append(dic)
                    if isinstance(obj, Wireframe):
                        dic["name"] = obj.name
                        for vertex in obj.vertices:
                            x, y, z = vertex[0], vertex[1], vertex[2]
                            lista.append([x, y, z])
                        dic["vertices"] = lista
                        objects.append(dic)
                for obj_dict in objects:
                    file.write(f'g {obj_dict["name"]}\n')
                    for vertex in obj_dict["vertices"]:
                        x , y , z = float(vertex[0]), float(vertex[1]), float(vertex[2])
                        file.write(f'v {x} {y} {z}\n')
                    file.write("\n")
            print(f"Arquivo {file_name} salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")
