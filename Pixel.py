class Pixel:
    def __init__(self, loc_x: int, loc_y: int, color: tuple, cluster_assignment=0):
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.color = color
        self.cluster_assignment = cluster_assignment

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pixel):
            if other.loc_x == self.loc_x and other.loc_y == self.loc_y and other.color == self.color:
                return True
        return False

    def __hash__(self) -> int:
        return hash((self.loc_x, self.loc_y, self.color))

    def __str__(self) -> str:
        return f'Centroid = [loc_x:{self.loc_x} loc_y:{self.loc_y} color:{self.color} ' \
               + f'cluster_assignment:{self.cluster_assignment}] '

