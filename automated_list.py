#Fixation V2.5
import matplotlib.pyplot as plt


def automated_list(monitor: int, eye: int, coord: list, steps_available: dict, param: list, step: list, id: str, around_whorl = list, config_bool = bool)-> list:
    """
    Create list of points to be shown.

    args:
        monitor: direction of monitor (1 = horziontal, 2 = vertical clockwise, 3 = vertical counter clockwise)
        eye: 1 = OD, 2 = OS
        coord: coordinate of starting point
        steps_available: dict with amount of steps available in every direction {'x_left', 'x_right', 'y_up', 'y_down'}
        param: parameters of sequence [width of rectangle, height of rectangle, distance between whorl and rectangle, steps nasally]
        step: pixel per step [in x direction, in y direction]
        id: identification of subject
        around_whorl: list of steps around whorl, from the configuration tool
        config_bool: bool, True if pattern was configurated, False if default pattern
    
    return:
        list of points in sequence
    
    save:
        plot of points
    """

    #create empty lists
    points = [coord]
    points_rect = []

    #define parameters for different monitor directions
    a, b, c = 0, 0, 0
    if monitor == 1:        #horizontal
        a = 1
    elif monitor == 2:      #vertical clockwise
        b = 1
    else:                   #vertical counter clockwise
        c = 1

    #define dimensions
    width = param[0]
    height = param[1]
    nasal = param[3]
    temporal = param[0] - param[3]
    caudal = param[1] + param[2]
    dist_whorl = param[2]

    #define steps
    step_nasal = [(a * (-1))** (eye + 1) , ((1 - a) * (-1) ** monitor)** (eye + 1) ]
    step_temp = [(-1) * i for i in step_nasal]
    step_up = [(a - 1) * (-1) ** monitor, a * (-1)]
    step_down = [(-1) * i for i in step_up]

    #createing empty list for movements
    movement_list_whorl = []
    movement_list = []

    #around the whorl
    adaption = {'up': step_up, 'nasal': step_nasal, 'temporal': step_temp, 'down': step_down}
    for item in around_whorl:
        movement_list_whorl .append(adaption[item])
    
    #Part between whorl and rectangle, if pattern configurated manually
    if not config_bool:
        #go max nasal
        if nasal > 1:
            for i in range(nasal // 2):
                if i != 0:
                    movement_list_whorl.append(step_nasal)
                movement_list.append(step_nasal)
        #go one down
        movement_list_whorl.append(step_down)

        if dist_whorl % 2 == 1: #if dist_whorl odd => -1
            dist_whorl -= 1
        for i in range(2,dist_whorl):
            if i % 2 == 0: #even rows
                gain = int(nasal + i * temporal / dist_whorl)
                movement_list_whorl.extend(gain * [step_temp])
            else:
                movement_list_whorl.extend(gain* [step_nasal])
            #go one down
            movement_list_whorl.append(step_down)

    #rectangle
    if width != 0 and height != 0:
        for row in range(height):
            if row != 0 or config_bool:
                movement_list.append(step_down)
            for i in range(width - 1):
                if row % 2 == 0:
                    movement_list.append(step_temp)
                else:
                    movement_list.append(step_nasal)

    #creat coordinates out of every direction
    #in the whorl region
    for i in range(len(movement_list_whorl)):
        point_x = movement_list_whorl[i][0] * step[2] + points[i][0] 
        point_y = movement_list_whorl[i][1] * step[3] + points[i][1] 
        points.append([point_x, point_y])
    #in the rectangle
    points_rect = [points[-1]]
    for i in range(len(movement_list)):
        point_x = movement_list[i][0] * step[0] + points_rect[i][0] 
        point_y = movement_list[i][1] * step[1] + points_rect[i][1] 
        points_rect.append([point_x, point_y])
    
    points.extend(points_rect[1:])
    
    x = [point[0] for point in points]
    y = [-point[1] for point in points]

    #initialise plot
    plt.style.use('default')
    fig, ax = plt.subplots()
    
    #delete ax-labels
    ax.set_xticks([])
    ax.set_yticks([])

    #create scatter plot   
    ax.scatter(x, y)

    #create annotations for every point
    annotations = [i for i in range(len(points)+1)]
    for xi, yi, text in zip(x, y, annotations):
        ax.annotate(text,
                    xy=(xi, yi), xycoords='data',
                    xytext=(5, 5), textcoords='offset points')

    # Show plot
    plt.savefig(f'saved/plots/raster_{id}.png')
    plt.close()

    return points
