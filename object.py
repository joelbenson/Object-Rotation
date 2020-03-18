from graphics import *
import math
import numpy as np
from copy import deepcopy

class Object():

    def __init__(self, window, num_vertices = None, vertices = None):
        self.window = window

        if (num_vertices):

            vertices = self.generate_random_object(num_vertices)

        elif(vertices == None):

            vertices = self.user_create_object_vertices(window)

        self.initial_vertices = vertices
        self.center_vertices()
        self.vertices = deepcopy(vertices)
        self.scaled_vertices = None
        self.projected_image = None
        self.image_lines = None
        self.init_diameter()

    def update_image(self):

        #Update scaled vertices
        self.scale_vertices()

        #Get orthographic projected of image
        self.update_projected_image()

        #Update image lines
        self.update_image_lines()

        return

    def update_image_lines(self):

        #Get image lines
        self.image_lines = []

        for i in range(len(self.projected_image)):
            for j in range(i + 1, len(self.projected_image)):
                p1 = Point(self.projected_image[i][0], self.projected_image[i][1])
                p2 = Point(self.projected_image[j][0], self.projected_image[j][1])

                self.image_lines.append(Line(p1, p2))

        return

    def draw(self):

        self.update_image()

        for line in self.image_lines:

            line.draw(self.window)

        return

    def redraw(self):

        #Undraw lines
        for line in self.image_lines:

            line.undraw()

        #Update image
        self.update_image()

        #Draw lines
        for line in self.image_lines:

            line.draw(self.window)

    def scale_vertices(self):

        #If object has no diameter, return
        if (len(self.vertices) < 2):

            self.scaled_vertices = self.vertices
            return

        SCALE = 0.7 * (self.window.width / 2) / self.diameter

        self.scaled_vertices = deepcopy(self.vertices)

        #Scale all dimensions that are not 0
        for i in range(len(self.scaled_vertices)):

            p = self.scaled_vertices[i]

            for d in range(len(p)):

                value = p[d]

                if (value != 0):

                    self.scaled_vertices[i][d] = value * SCALE

        return

    def rotate(self, rotation):

        ROTATION_RATE = 10

        x_axis_rotation = rotation[1] * ROTATION_RATE
        y_axis_rotation = rotation[0] * ROTATION_RATE

        if (abs(x_axis_rotation) > abs(y_axis_rotation)):
            y_axis_rotation = 0
        else:
            x_axis_rotation = 0

        prev_vertices = deepcopy(self.vertices)

        for i, v in enumerate(self.vertices):

            prev_v = prev_vertices[i]

            #rotate x axis
            v[1] = prev_v[1]* math.cos(x_axis_rotation) - prev_v[2] * math.sin(x_axis_rotation)
            v[2] = prev_v[1] * math.sin(x_axis_rotation) + prev_v[2] * math.cos(x_axis_rotation)

            prev_v = deepcopy(v)

            #rotate y axis
            v[0] = prev_v[0] * math.cos(y_axis_rotation) + prev_v[2] * math.sin(y_axis_rotation)
            v[2] = prev_v[2] * math.cos(y_axis_rotation) - prev_v[0] * math.sin(y_axis_rotation)

        return

    def translate(self, translation):

        for v in self.vertices:
            v[0] += translation[0]
            v[1] -= translation[1]

        return

    def update_projected_image(self):

        self.projected_image = []

        for v in self.scaled_vertices:

            self.projected_image.append([v[0], v[1]])

        return

    def init_diameter(self):

        diameter = 0

        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):

                v = self.vertices[i]
                w = self.vertices[j]

                distance = ((v[0] - w[0])**2  + (v[1] - w[1])**2 + (v[2] - w[2])**2)**0.5
                diameter = max([diameter, distance])

        self.diameter = diameter

    def generate_object(self, n):

            vertices = []
            count = 0

            alpha = 4 * math.pi / n
            d = alpha ** 0.5

            M_theta = round(math.pi / d)

            d_theta = math.pi / M_theta
            d_psi = alpha / d_theta

            for m in range(M_theta):

                theta = math.pi * (m + 0.5) / M_theta
                M_psi = round(2 * math.pi * math.sin(theta) / d_psi)

                for n in range(M_psi):

                    psi = 2 * math.pi * n / M_psi

                    x = math.sin(theta) * math.cos(psi)
                    y = math.sin(theta) * math.sin(psi)
                    z = math.cos(theta)

                    vertices.append([x, y, z])
                    count += 1


            return vertices

    def generate_random_object(self, n):

        vertices = []

        for i in range(n):

            theta = np.random.uniform(0, math.pi)
            psi = np.random.uniform(0, 2 * math.pi)

            x = math.sin(theta) * math.cos(psi)
            y = math.sin(theta) * math.sin(psi)
            z = math.cos(theta)

            vertices.append([x, y, z])

        return vertices




    def user_create_object_vertices(self, window):

        limit = window.height
        vertices = []

        print('How many vertices would you like your object to have?')

        n = int(input())

        for i in range(n):

            print("Click vertex location for x and y value")

            mouse = window.getMouse()
            x = mouse.x
            y = mouse.y

            x = float(x) / limit
            y = float(y) / limit

            print("Enter a corresponding z value in the range [{}, {}]".format(-limit, limit))

            z = int(input()) / limit

            vertices.append([x, y, z])

        return vertices

    def center_vertices(self):

        x_avg = 0
        y_avg = 0
        z_avg = 0

        n = len(self.initial_vertices)

        for v in self.initial_vertices:

            x_avg += v[0] / n
            y_avg += v[1] / n
            z_avg += v[2] / n

        for v in self.initial_vertices:

            v[0] -= x_avg
            v[1] -= y_avg
            v[2] -= z_avg
