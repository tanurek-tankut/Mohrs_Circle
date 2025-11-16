import tkinter as tk
import math


def user_input(root):
    """
    Creates a canvas with frame on main window. 
    Creates entries and labels to take info from user. 
    Takes raw values directly came from user.
    """

    global entry_x_normal, entry_y_normal, entry_xy_shear, entry_theta # Gived variables

    frame = tk.Frame(root, bd=1, bg="#666666")
    frame.grid(row=0, column=0, padx=820, pady=410, sticky='nw')

    input_canvas = tk.Canvas(frame, width=380, height=270, bg="#CCCCCC")
    input_canvas.grid(padx=0, pady=0, sticky='nw')

    # Texts
    input_canvas.create_text(125, 30, text="σₓ Normal Force:", font=("Arial", 12, "italic"), fill="#404040")
    input_canvas.create_text(125, 60, text="σʸ Normal Force:", font=("Arial", 12, "italic"), fill="#404040")
    input_canvas.create_text(125, 90, text="𝜏ₓʸ Shear Force:", font=("Arial", 12, "italic"), fill="#404040")
    input_canvas.create_text(150, 150, text="θ Angle:", font=("Arial", 12, "italic"), fill="#404040")

    # Entries (Default values are 0 for all)
    entry_x_normal = tk.Entry(input_canvas)
    entry_x_normal.insert(0, "0")
    input_canvas.create_window(245, 30, window=entry_x_normal, width=100)

    entry_y_normal = tk.Entry(input_canvas)
    entry_y_normal.insert(0, "0")
    input_canvas.create_window(245, 60, window=entry_y_normal, width=100)

    entry_xy_shear = tk.Entry(input_canvas)
    entry_xy_shear.insert(0, "0")
    input_canvas.create_window(245, 90, window=entry_xy_shear, width=100)

    entry_theta = tk.Entry(input_canvas)
    entry_theta.insert(0, "0")
    input_canvas.create_window(245, 150, window=entry_theta, width=100)


def point_calculations():
    """
    Read entries coming from user_input() and turn them into usable values.
    """

    global entry_x_normal, entry_y_normal, entry_xy_shear, entry_theta # Recieved variables
    global sigma_x, sigma_y, sigma_x_new, sigma_y_new, tau_xy_new, R_radius, C_center, radian_theta# Gived variables

    # Turn Etries into floats
    sigma_x = float(entry_x_normal.get())
    sigma_y = float(entry_y_normal.get())
    tau_xy = float(entry_xy_shear.get())
    theta = float(entry_theta.get())
    radian_theta = math.radians(theta)

    # Prints User Input
    print("=== User Inputs ===")
    print(f"σx (x normal) : {sigma_x}")
    print(f"σy (y normal) : {sigma_y}")
    print(f"τxy (x-y shear)  : {tau_xy}")
    print(f"θ  (degree) : {theta}")

    # Prints C center point position
    C_center = ((sigma_x + sigma_y) / 2, 0)
    print("=== Location of C Point ===")
    print(f"center: {C_center}")

    # Prints R radius length
    R_radius = math.sqrt((sigma_x - (sigma_x + sigma_y) / 2) ** 2 + tau_xy ** 2)
    print("=== Radius R length ===")
    print(f"radius: {R_radius}")

    """ 
    # Alpha circle starting degree
    alpha_radian = math.atan2(tau_xy, (sigma_x - (sigma_x + sigma_y) / 2))
    print("=== Alpha in Radian ===")
    print(f"alpha radian: {alpha_radian}")

    alpha_degree = math.degrees(alpha_radian)
    print("=== Alpha in Degree ===")
    print(f"alpha degree: {alpha_degree}") 
    """

    """ === Components of Rotating Object === """
    cos2 = math.cos(2*radian_theta)
    sin2 = math.sin(2*radian_theta)
    # Sigma X component after Theta degree rotation
    sigma_x_new = (sigma_x + sigma_y)/2 + (sigma_x - sigma_y)/2 * cos2 + tau_xy * sin2
    # Sigma Y component after Theta degree rotation 
    sigma_y_new = (sigma_x + sigma_y)/2 - (sigma_x - sigma_y)/2 * cos2 - tau_xy * sin2
    # Tau XY component after Theta degree rotation
    tau_xy_new = -(sigma_x - sigma_y)/2 * sin2 + tau_xy * cos2

    # Prints Rotated A' point
    A_rotated = (sigma_x_new, tau_xy_new)
    print("=== Rotated A Point ===")
    print(f"A': {A_rotated}")

    # Pritnts Rotated B' point
    B_rotated = (sigma_y_new, - tau_xy_new)
    print("=== Rotated B Point ===")
    print(f"B': {B_rotated}")

    # All recieved entries bind for updates
    entry_x_normal.bind("<KeyRelease>", update)
    entry_y_normal.bind("<KeyRelease>", update)
    entry_xy_shear.bind("<KeyRelease>", update)
    entry_theta.bind("<KeyRelease>", update)


def mohrs_diagram(root):
    """
    Creates a canvas with frame on main window.
    Creates a cartesian system with grid and labels.
    """

    global circle_canvas, midpoint # Gived variables

    frame = tk.Frame(root, bd=4, bg="#666666")
    frame.grid(row=0, column=0, padx=30, pady=30, sticky='nw')

    circle_canvas = tk.Canvas(frame, width=700, height=700, bg="white")
    circle_canvas.grid(padx=0, pady=0, sticky='nw')

    # Grid
    cell_size = 25
    for x in range(0, 700, cell_size):
        for y in range(0, 700, cell_size):
            circle_canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="#CCCCCC")

    # Sigma-Tau cartesian system
    midpoint = 350

    circle_canvas.create_line(0, midpoint, 700, midpoint, fill="#404040", width=3)  # σ line
    circle_canvas.create_line(midpoint, 0, midpoint, 700, fill="#404040", width=3) # 𝜏 line
    circle_canvas.create_text(670, 370, text="σ", font=("Arial", 22, "italic")) # σ mark
    circle_canvas.create_text(370, 30, text="𝜏", font=("Arial", 22, "italic")) # 𝜏 mark


def create_circle():    
    """
    Delete old drawings for each frame.
    Creates new Mohr's Circle for new input coming from point_calculations().
    """
    
    global circle_canvas, midpoint, sigma_x_new, sigma_y_new, tau_xy_new, R_radius # Recieved variables

    # Clearing temporal lines on canvas for next frame
    circle_canvas.delete("dynamic")

    # Drawing line between A and B points
    circle_canvas.create_line(
    midpoint + sigma_x_new, midpoint + tau_xy_new,
    midpoint + sigma_y_new, midpoint - tau_xy_new,
    fill="#404040", width=2, tags="dynamic"
    )

    # Drawing Mohr's Circle
    circle_canvas.create_oval(
    midpoint + (sigma_x + sigma_y) / 2 - R_radius, midpoint + 0 - R_radius,
    midpoint + (sigma_x + sigma_y) / 2 + R_radius, midpoint + 0 + R_radius,
    width=2, fill="", tags="dynamic"
    )

    """  === Creating Points on Diagram ===  """
    # Drawing Points on Canvas
    circle_canvas.create_oval(
    midpoint + sigma_x_new - 5, midpoint + tau_xy_new - 5,  # Rotated A' point on diagram
    midpoint + sigma_x_new + 5, midpoint + tau_xy_new + 5,
    fill="#6CA6CD", tags="dynamic"
    )

    circle_canvas.create_oval(
    midpoint + sigma_y_new - 5, midpoint - tau_xy_new - 5,  # Rotated B' point on diagram
    midpoint + sigma_y_new + 5, midpoint - tau_xy_new + 5,
    fill="#6CA6CD", tags="dynamic"
    )

    circle_canvas.create_oval(
    midpoint + (sigma_x + sigma_y) / 2 - 5, midpoint - 5,   # C point on daigram
    midpoint + (sigma_x + sigma_y) / 2 + 5, midpoint + 5,
    fill="#CCCCCC", tags="dynamic"
    )


def free_body_diagram(root):
    """
    Creates a canvas with frame on main window.
    Creates a cartesian system for free body diagram.
    """

    global object_canvas # Gived variable

    frame = tk.Frame(root, bd=4, bg="#666666")
    frame.grid(row=0, column=0, padx=800, pady=30, sticky='nw')

    object_canvas = tk.Canvas(frame, width=420, height=300, bg="#CCCCCC")
    object_canvas.grid(padx=0, pady=0, sticky='nw')

    # x-y cartesian system
    object_frame_midpoint_x = 210
    object_frame_midpoint_y = 150

    object_canvas.create_line(40, object_frame_midpoint_y, 380, object_frame_midpoint_y, fill="#8C8C8C", width=2)  # X line
    object_canvas.create_line(object_frame_midpoint_x, 40, object_frame_midpoint_x, 260, fill="#8C8C8C", width=2) # Y line
    object_canvas.create_text(400, 150, text="x", fill="#8C8C8C", font=("Arial", 8, "italic")) # x mark
    object_canvas.create_text(210, 15, text="y", fill="#8C8C8C", font=("Arial", 8, "italic")) # y mark


def create_object():
    """
    Delete old drawings for each frame.
    Creates object to show rotation on free_body_diagram() canvas.
    Rotate object with rotation values coming from point_calculations().
    Uses rotate_point() to rotate object.
    """
    
    global object_canvas, radian_theta # Recieved variables
    global half, center_x, center_y # Gived variables

    # Clearing temporal lines on canvas for next frame
    object_canvas.delete("dynamic") 

    size = 70
    center_x = 210
    center_y = 150
    half = size / 2

    # Corner Points at the Beginning
    corner_points = [
        (center_x - half, center_y - half), # Top Left
        (center_x + half, center_y - half), # Top Right
        (center_x + half, center_y + half), # Bottom Left
        (center_x - half, center_y + half)  # Bottom Right
    ]
    # Corner Points Calculation After Rotation
    rotated_corner_points = []
    for x, y in corner_points:
        (rotated_x, rotated_y) = rotate_point(x, y, center_x, center_y, radian_theta)
        rotated_corner_points.append((rotated_x, rotated_y))

    # Corner Point Positions in Flat Form for Creating Rectangle
    flat_points = [
        rotated_corner_points[0][0], rotated_corner_points[0][1],  # Top Left
        rotated_corner_points[1][0], rotated_corner_points[1][1],  # Top Right
        rotated_corner_points[2][0], rotated_corner_points[2][1],  # Bottom Right
        rotated_corner_points[3][0], rotated_corner_points[3][1]   # Bottom Left
    ]
    """
    flat_points = [coord for point in rotated_corner_points for coord in point]  ---  (shorter alternative for flat points)
    """
    object_canvas.create_polygon(
    flat_points, 
    outline="#404040", fill="#6CA6CD",
    width=2, tags="dynamic"
    )


def create_vector_arrows():
    global object_canvas, half, center_x, center_y, sigma_x_new, sigma_y_new, tau_xy_new, radian_theta # Recieved Variables

    object_canvas.delete("stress_vectors")
    arrow_length = 70

    # Sigma arrows (X/Y)
    sigma_arrows = [
        {"start": (center_x, center_y - half), "end": (center_x, center_y - half - arrow_length), "value": sigma_y_new},
        {"start": (center_x, center_y + half), "end": (center_x, center_y + half + arrow_length), "value": sigma_y_new},
        {"start": (center_x + half, center_y), "end": (center_x + half + arrow_length, center_y), "value": sigma_x_new},
        {"start": (center_x - half, center_y), "end": (center_x - half - arrow_length, center_y), "value": sigma_x_new}
    ]

    # Create Sigma vectors
    for arrow in sigma_arrows:
        if arrow["value"] == 0:
            continue
        x0, y0 = arrow["start"]
        x1, y1 = arrow["end"]
        if arrow["value"] < 0:
            x0, y0, x1, y1 = x1, y1, x0, y0
        x0_rot, y0_rot = rotate_point(x0, y0, center_x, center_y, radian_theta)
        x1_rot, y1_rot = rotate_point(x1, y1, center_x, center_y, radian_theta)

        object_canvas.create_line(
            x0_rot, y0_rot, x1_rot, y1_rot,
            arrow=tk.LAST, fill="#404040", width=3,
            arrowshape=(12, 15, 6), tags="stress_vectors"
        )

    # Create Tau Vectors
    if tau_xy_new != 0:

        mid_left   = (center_x - half, center_y)
        mid_right  = (center_x + half, center_y)
        mid_top    = (center_x, center_y - half)
        mid_bottom = (center_x, center_y + half)

        tau_pairs_pos = [
            {"start": mid_left,   "dir": (0,  half)},
            {"start": mid_bottom, "dir": (-half, 0)},
            {"start": mid_right,  "dir": (0, -half)},
            {"start": mid_top,    "dir": (half, 0)}
        ]

        tau_pairs_neg = [
            {"start": mid_left,   "dir": (0, -half)},
            {"start": mid_top,    "dir": (-half, 0)},
            {"start": mid_right,  "dir": (0,  half)},
            {"start": mid_bottom, "dir": (half, 0)}
        ]

        tau_pairs = tau_pairs_pos if tau_xy_new > 0 else tau_pairs_neg

        for arrow in tau_pairs:
            x0, y0 = arrow["start"]
            dx, dy = arrow["dir"]
            x1, y1 = x0 + dx, y0 + dy

            x0r, y0r = rotate_point(x0, y0, center_x, center_y, radian_theta)
            x1r, y1r = rotate_point(x1, y1, center_x, center_y, radian_theta)

            object_canvas.create_line(
                x0r, y0r, x1r, y1r,
                arrow=tk.LAST,
                width=3,
                fill="#404040",
                arrowshape=(12, 15, 6),
                tags="stress_vectors"
            )


def update(event):
    """
    Run fucntions to keep drawings and calculations up-to-date after each new input.
    """
    
    point_calculations()
    create_circle()
    create_object()
    create_vector_arrows()


def rotate_point(point_x, point_y, center_x, center_y, radian_theta):
    """
    Runs by other functions to calculate rotation of points.
    """

    # Location respect to the canvas midpoints
    local_x = point_x - center_x
    local_y = point_y - center_y

    # Rotated X and Y components
    rotated_x = center_x + local_x * math.cos(radian_theta) - local_y * math.sin(radian_theta)
    rotated_y = center_y + local_x * math.sin(radian_theta) + local_y * math.cos(radian_theta)

    return rotated_x, rotated_y


def main():

    root = tk.Tk()
    root.title("Mohr's Circle")
    root.geometry("1280x768")
    root.resizable(width=False, height=False)
    root.configure(background="#CCCCCC")

    user_input(root)
    point_calculations()
    mohrs_diagram(root)
    free_body_diagram(root)

    root.mainloop()


# Self-Run Block
if __name__ == "__main__":
    main()