import os

dir = os.path.dirname(__file__) + "/"

print(dir)

scripts = ["GUI_crowd_MapPanel.py", "GUI_crowd_ParamPanel.py", "GUI_crowd_SimulationPanel.py"]

for script in scripts:
    filename = dir + script
    print("EXECUTING", filename, "...")
    exec(compile(open(filename).read(), filename, 'exec'))
