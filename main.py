from graphics import *
from object import Object
import time


def main():

    #WINDOW
    WINDOW_SIZE = float(750)
    FRAME_DELAY = 0

    #OBJECT
    NUM_VERTICES = int(input("How many vertices should the object have?"))

    #Initialize window
    window = GraphWin(title="Object Rotation", width=WINDOW_SIZE, height=WINDOW_SIZE, autoflush=False)
    window.setCoords(-int(WINDOW_SIZE/2), -int(WINDOW_SIZE/2), int(WINDOW_SIZE/2), int(WINDOW_SIZE/2))

    mouse = MouseTracker()
    window.bind('<Motion>', mouse.track)

    #Initialize object
    object = Object(window, num_vertices = NUM_VERTICES)

    #Draw object to window
    object.draw()

    rotating = False
    initial_mouse_position = None

    text_size = int(min(max((WINDOW_SIZE / 40.0), 5), 36))
    prompt_text = Text(Point(0, 0.4 * WINDOW_SIZE), "Click to begin rotating")
    prompt_text.setTextColor('black')
    prompt_text.setSize(text_size)
    prompt_text.draw(window)

    #Until user quits the window
    while(not window.isClosed()):

        if (rotating == False):

            prompt_text.setTextColor('black')

        else:
            prompt_text.setTextColor('white')


        clicked = False

        #Check if user has clicked the mouse
        new_user_click = window.checkMouse()
        if (new_user_click): clicked = True

        #If user clicks while not rotating, start tracking movement
        if (rotating == False and clicked):

            rotating = True
            initial_mouse_position = [mouse.x, mouse.y]

        #If user clicks while rotating, stop tracking movement
        elif (rotating == True and clicked):

            rotating = False

        #If rotating, get rotation amount
        if (rotating == True):

            if (initial_mouse_position[0] == None or initial_mouse_position[1] == None):
                initial_mouse_position[0] = mouse.x
                initial_mouse_position[1] = mouse.y
                continue

            movement_amount_x = (mouse.x - initial_mouse_position[0]) / (WINDOW_SIZE / 2.0)
            initial_mouse_position[0] = mouse.x
            movement_amount_y = (mouse.y - initial_mouse_position[1]) / (WINDOW_SIZE / 2.0)
            initial_mouse_position[1] = mouse.y

            #object.translate((movement_amount_x, movement_amount_y))
            object.rotate((movement_amount_x, movement_amount_y))

        object.redraw()

        update()

        time.sleep(FRAME_DELAY)

    return


class MouseTracker():

    def __init__(self):
        self.x = None
        self.y = None

    def track(self, event):

        if (event.x != None or event.y != None):
            self.x = event.x
            self.y = event.y

        return



if __name__ == "__main__":
    main()
