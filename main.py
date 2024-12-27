import matplotlib.pyplot as plt
import numpy as np

# Function to parse a G-code file and extract XYZ coordinates and extrusion for a given layer
def parse_gcode_layer(file_path, target_z):
    coordinates = []
    current_z = None
    previous_e = None

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("G1"):
                parts = line.split()
                x = y = z = e = None

                for part in parts:
                    if part.startswith("X"):
                        x = float(part[1:])
                    elif part.startswith("Y"):
                        y = float(part[1:])
                    elif part.startswith("Z"):
                        z = float(part[1:])
                    elif part.startswith("E"):
                        e = float(part[1:])

                if z is not None:
                    current_z = z

                if current_z == target_z and x is not None and y is not None:
                    extrusion = e - previous_e if previous_e is not None and e is not None else 0
                    coordinates.append((x, y, extrusion))

                if e is not None:
                    previous_e = e

    return coordinates

# Function to calculate the center of mass (COM) for a set of points weighted by extrusion
def calculate_center_of_mass(points):
    if not points:
        return None

    total_weight = 0
    weighted_x_sum = 0
    weighted_y_sum = 0

    for x, y, extrusion in points:
        if extrusion > 0:  # Only consider points with extrusion
            total_weight += extrusion
            weighted_x_sum += x * extrusion
            weighted_y_sum += y * extrusion

    if total_weight == 0:
        return None

    com_x = weighted_x_sum / total_weight
    com_y = weighted_y_sum / total_weight
    return com_x, com_y

# Function to visualize the G-code paths and the center of mass
def visualize_gcode_layer(points, com):
    if not points:
        print("No points to visualize.")
        return

    x_coords = [x for x, y, e in points]
    y_coords = [y for x, y, e in points]

    plt.figure(figsize=(10, 10))
    plt.plot(x_coords, y_coords, label="Toolpath", color="blue", marker=".", linestyle="-", markersize=3)

    if com:
        plt.plot(com[0], com[1], 'ro', label="Center of Mass")

    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("G-code Layer Visualization")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.show()

# Main execution
if __name__ == "__main__":
    # Specify the G-code file path and target layer height
    file_path = "example.gcode"  # Replace with your G-code file
    target_z = 3  # Replace with the Z-height of the layer you want to analyze

    # Parse the G-code file to extract coordinates for the target layer
    

    layer_points = parse_gcode_layer(file_path, target_z)

    # Calculate the center of mass for the extracted points
    com = calculate_center_of_mass(layer_points)

    # Print the center of mass
    if com:
        print(f"Center of Mass for Z={target_z}: (X={com[0]:.3f}, Y={com[1]:.3f})")
    else:
        print(f"No data found for Z={target_z}")

    # Visualize the G-code layer and center of mass
    visualize_gcode_layer(layer_points, com)
