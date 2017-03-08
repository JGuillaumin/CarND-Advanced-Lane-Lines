import numpy as np

settings = dict()

settings["xgrad_thr"] = (40,130)
settings["s_thr"] = (120, 255)
settings["l_thr"] = (45, 255)

settings["ROI_ptA"] = (560, 450)
settings["ROI_ptB"] = (720, 450)

settings["corners"] = np.float32([[190, 720], [589, 457], [698, 457], [1145, 720]])
settings["offset"] = [150, 0]

settings["window_radius"] = 200
settings["v_offset"] = 50
settings["h_offset"] = 50
settings["nb_steps"] = 6