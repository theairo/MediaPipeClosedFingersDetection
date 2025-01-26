import math

def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates the angle between three different landmarks considering the x, y, and z coordinates.
    Args:
        landmark1: The first landmark containing the x, y, and z coordinates.
        landmark2: The second landmark containing the x, y, and z coordinates.
        landmark3: The third landmark containing the x, y, and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.
    '''
    # Get the x, y, z coordinates of the landmarks
    id1, x1, y1 = landmark1
    id2, x2, y2 = landmark2
    id3, x3, y3 = landmark3

    # Compute the vectors from landmark2 to landmark1 and landmark2 to landmark3
    vector1 = [x1 - x2, y1 - y2]
    vector2 = [x3 - x2, y3 - y2]

    # Compute the dot product of the two vectors
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

    # Compute the magnitudes of the vectors
    magnitude_vector1 = math.sqrt(sum(v1 ** 2 for v1 in vector1))
    magnitude_vector2 = math.sqrt(sum(v2 ** 2 for v2 in vector2))

    # Compute the cosine of the angle using the dot product formula
    cos_angle = dot_product / (magnitude_vector1 * magnitude_vector2)

    # Ensure the cosine value is in the range [-1, 1] to avoid errors due to floating point precision
    cos_angle = max(-1, min(1, cos_angle))

    # Compute the angle in radians and convert it to degrees
    angle = math.degrees(math.acos(cos_angle))

    # Return the calculated angle
    return angle
