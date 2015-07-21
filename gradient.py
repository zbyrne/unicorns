from PIL import Image
from math import sqrt
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])
Colour = namedtuple('Colour', ['r', 'g', 'b'])
GradientNode = namedtuple('GradientNode', ['point', 'colour'])


def norm(p1, p2):
    x = abs(p1.x - p2.x)
    y = abs(p1.y - p2.y)
    return sqrt(x**2 + y**2)


def weighted_colour(point, node1, node2):
    dist1 = norm(point, node1.point)
    dist2 = norm(point, node2.point)
    norm_dist1 = dist1 / (dist1 + dist2)
    norm_dist2 = dist2 / (dist1 + dist2)
    r = int(norm_dist1 * node1.colour.r + norm_dist2 * node2.colour.r)
    g = int(norm_dist1 * node1.colour.g + norm_dist2 * node2.colour.g)
    b = int(norm_dist1 * node1.colour.b + norm_dist2 * node2.colour.b)
    return Colour(r, g, b)


def gradient2(img, node1, node2):
    width, height = img.size
    for x in xrange(width):
        for y in xrange(height):
            img.putpixel((x, y), weighted_colour(Point(x, y), node1, node2))


def get_node_pairs(nodes):
    pairs = []
    mod_list = list(nodes)
    for a in nodes:
        for b in mod_list:
            if a is not b:
                pairs.append((a, b))
        mod_list.remove(a)
    return pairs

def gradient(img, *nodes):
    width, height = img.size
    node_pairs = get_node_pairs(nodes)
    for x in xrange(width):
        for y in xrange(height):
            a_r = 0
            a_g = 0
            a_b = 0
            for a, b in node_pairs:
                r, g, b = weighted_colour(Point(x, y), a, b)
                a_r += r
                a_g += g
                a_b += b
            colour = Colour(a_r / len(node_pairs),
                            a_g / len(node_pairs),
                            a_b / len(node_pairs))
            img.putpixel((x, y), colour)


img = Image.new("RGB", (200, 200))
node1 = GradientNode(Point(0, 0), Colour(255, 0, 0))
node2 = GradientNode(Point(200, 200), Colour(0, 255, 0))
node3 = GradientNode(Point(100, 100), Colour(0, 0, 255))

gradient(img, node1, node2, node3)
img.save("grad.png")
