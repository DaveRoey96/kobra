from roboflow import Roboflow
rf = Roboflow(api_key="Ab2c46agi5lpraRHlkE2")
project = rf.workspace("test").project("snakes-4estp-4go9n")
dataset = project.version(2).download("yolov8")


if __name__ == '__main__':
    print(dataset)