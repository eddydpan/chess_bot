import cv2
import apriltag
import numpy as np
import shapely.geometry as geom
from shapely.prepared import prep
from skimage.metrics import structural_similarity
from enum import Enum
import time
 

class BoardView():
    class Corner(Enum):
        # ROBOT_L = 96
        PLAYER_R = 98
        PLAYER_L = 99
        ROBOT_R = 97
    
    BoardCorners = {
        # "ROBOT_L": 0,
        "PLAYER_R": 2,
        "PLAYER_L": 1,
        "ROBOT_R": 3
    }

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(0, 1)

        _, self.init_frame = self.cap.read()
        _, self.init_frame = self.cap.read()

        self.H, self.W = self.init_frame.shape[:2]
        self.CENTER = (self.W // 2, self.H // 2)

        self.frame = cv2.cvtColor(self.init_frame, cv2.COLOR_BGR2GRAY)

        # rotate and translate frame for best view
        self.frame = self.__rotate_frame(self.frame, 25)

        # last saved board state
        self.last_frame = self.frame

        self.board_cells = {}
    

    def show_frame(self):
        running = True

        while running:
            _, view_frame = self.cap.read()
            cv2.imshow("test", view_frame)

            if cv2.waitKey(1) == ord("q"):
                running = False

        self.cap.release()
        cv2.destroyAllWindows()

        
    
    def __find_tags(self, draw = False):
        detector = apriltag.Detector()
        _, self.init_frame = self.cap.read()
        self.init_frame = self.__rotate_frame(self.init_frame, 25)
        self.frame = cv2.cvtColor(self.init_frame, cv2.COLOR_BGR2GRAY)

        april_tags = detector.detect(self.frame)

        tag_dict = {}

        for tag in april_tags:
            print(tag.tag_id)
            tag_dict[self.Corner(tag.tag_id).name] = tag.corners

            # if draw:
            #     cv2.polylines(self.frame, [tag.corners.astype(int)], True, (0, 255, 0), 2)
            #     self.show_frame()
        print(tag_dict)
        return tag_dict
    
    def __get_corners(self, tag_dict):
        board_corners = []

        for corner, idx in self.BoardCorners.items():
            board_corners.append(tag_dict[corner][idx])
        
        return board_corners

    def create_grid(self, corners):
        nx = 9
        ny = 9

        square = geom.Polygon(corners)
        min_x, min_y, max_x, max_y = square.bounds

        grid_x = np.linspace(min_x, max_x, nx)
        grid_y = np.linspace(min_y, max_y, ny)

        grid = []
        for ix in range(len(grid_x) - 1):
            for iy in range(len(grid_y) - 1):
                print("making cell")
                cell = geom.Polygon([
                    [grid_x[ix], grid_y[iy]],
                    [grid_x[ix], grid_y[iy + 1]],
                    [grid_x[ix + 1], grid_y[iy + 1]],
                    [grid_x[ix + 1], grid_y[iy]]
                ])
                grid.append(cell)
        
        # i feel like odds are i dont need this line
        # grid = list(filter(prep(square).intersects, grid))

        for cell in grid:
            ext_pts = cell.exterior.coords
            pts = np.array(ext_pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            # cv2.polylines(self.frame, [pts], True, (0, 255, 0), 2)

        # cv2.imshow('frame', self.frame)
        # cv2.waitKey(0)  # Wait for a key press
        # cv2.destroyAllWindows()  # Close the window

        letters = "hgfedcba"
        idx = 0
        num = 0

        for cell in grid:
            # i think this is gonna name them right but we'll see
            cell_label = letters[idx] + str(num + 1)
            self.board_cells[cell_label] = cell

            num += 1
            if num == 8:
                num = 0
                idx += 1
            
            
        
        print(self.board_cells.keys())
        print(self.board_cells.values())

    
    def locate_board(self, draw = False):
        tag_dict = self.__find_tags(draw)
        
        while(len(tag_dict) != 3):
            print(len(tag_dict))
            print("thats bad")

            tag_dict = self.__find_tags()
        
        print("escaped????")
        corners = self.__get_corners(tag_dict)
        self.create_grid(corners)
    
    
    def update_board_state(self):
        print("taking new image!!")
        for _ in range(4):
            self.cap.read()
        _, frame = self.cap.read()
        frame = self.__rotate_frame(frame, 25)
        self.last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def find_moved_piece(self, draw = False):
        for _ in range(4):
            self.cap.read()


        _, init_frame = self.cap.read()
        init_frame = self.__rotate_frame(init_frame, 25)
        new_frame = cv2.cvtColor(init_frame, cv2.COLOR_BGR2GRAY)

        _, diff = structural_similarity(self.last_frame, \
            new_frame, full = True)

        # cv2.imshow('Difference', diff)

        cell_diffs = {}

        for cell_name, cell in self.board_cells.items():
            exterior_pts = cell.exterior.coords
            pts = np.array(exterior_pts, np.int32)
            pts = pts.reshape((-1, 1, 2))

            min_x, min_y, max_x, max_y = cell.bounds
            cell_diff = 0

            for x in range(int(min_x), int(max_x)):
                for y in range(int(min_y), int(max_y)):
                    cell_diff += diff[y][x]
            
            cell_diffs[cell_name] = cell_diff
        
        print(cell_diffs)
        sorted_cells = sorted(cell_diffs, key = cell_diffs.get)

        for i in range(0, 2):
            ext_pts = self.board_cells[sorted_cells[i]].exterior.coords
            pts = np.array(ext_pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(diff, [pts], True, (0, 0, 255), 5)
        
        cv2.imshow('diff', diff)
        cv2.waitKey(0)  # Wait for a key press
        cv2.destroyAllWindows()  # Close the window

        return sorted_cells[0], sorted_cells[1]

    def __rotate_frame(self, frame, theta):
        R = cv2.getRotationMatrix2D(self.CENTER, theta, 1.0)
        return cv2.warpAffine(frame, R, (self.W, self.H))
    
    def __translate_frame(self, frame, x, y):
        T = np.float32([[1, 0, x], [0, 1, y]])
        return cv2.warpAffine(frame, T, (self.W, self.H))
    
