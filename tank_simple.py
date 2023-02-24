import random


class Tank:
    def __init__(self):
        # tank coordinates
        self.x = 430
        self.y = 230
        self.direction = str()
        self.shots_north = 0
        self.shots_east = 0
        self.shots_south = 0
        self.shots_west = 0
        self.total_shots = 0

        # target coordinates
        self.t_x = int()
        self.t_y = int()
        self.target_pos = self.make_target()
        print(f"target at {self.target_pos}")

    def make_target(self):
        self.t_x = random.randint(-5, 5)
        self.t_y = random.randint(-5, 5)
        self.target_pos = (self.t_x, self.t_y)
        return self.target_pos

    def go_forward(self):
        self.y += 1
        self.direction = "North"
        print(f"moved {self.direction}")

    def go_right(self):
        self.x += 1
        self.direction = "East"
        print(f"moved {self.direction}")

    def go_backward(self):
        self.y -= 1
        self.direction = "South"
        print(f"moved {self.direction}")

    def go_left(self):
        self.x -= 1
        self.direction = "West"
        print(f"moved {self.direction}")

    def shoot(self):
        match self.direction:
            case "North":
                self.shots_north += 1
                self.total_shots += 1
                print(f"fired a shot to the {self.direction}")
                if (self.x, self.y) == (self.t_x, self.t_y - 1):
                    print(f"target at {self.target_pos} destroyed")
                    self.make_target()
                    print(f"new target at {self.target_pos}")
            case "East":
                self.shots_east += 1
                self.total_shots += 1
                print(f"fired a shot to the {self.direction}")
                if (self.x, self.y) == (self.t_x - 1, self.t_y):
                    print(f"target at {self.target_pos} destroyed")
                    self.make_target()
                    print(f"new target at {self.target_pos}")
            case "South":
                self.shots_south += 1
                self.total_shots += 1
                print(f"fired a shot to the {self.direction}")
                if (self.x, self.y) == (self.t_x, self.t_y + 1):
                    print(f"target at {self.target_pos} destroyed")
                    self.make_target()
                    print(f"new target at {self.target_pos}")
            case "West":
                self.shots_west += 1
                self.total_shots += 1
                print(f"fired a shot to the {self.direction}")
                if (self.x, self.y) == (self.t_x + 1, self.t_y):
                    print(f"target at {self.target_pos} destroyed")
                    self.make_target()
                    print(f"new target at {self.target_pos}")
            case _:
                print("you must move before shooting")

    def get_info(self):
        print(f"INFO target coordinates: {self.target_pos}")
        print(f"INFO current direction: {self.direction}")
        print(f"INFO tank coordinates: {(self.x, self.y)}")
        print(f"INFO total shots: {self.total_shots}")
        print(
            f"INFO shots fired at direction:\n* North {self.shots_north}\n* East {self.shots_east}\n* South {self.shots_south}\n* West {self.shots_west}")


tank1 = Tank()
print("controls:\nf - go forward\nr - go right\nb - go backward\nl - go left\ns - shoot\n0 - menu\n")
while True:

    user_command = input("command: ")

    match user_command:
        case "f":
            tank1.go_forward()
        case "r":
            tank1.go_right()
        case "b":
            tank1.go_backward()
        case "l":
            tank1.go_left()
        case "s":
            tank1.shoot()
        case "0":
            menu_choice = input(
                "choose an option:\n1 - show info\n2 - return to the game\n3 - exit\n")

            match menu_choice:
                case "1":
                    tank1.get_info()
                case "2":
                    continue
                case "3":
                    break
        case _:
            print("no such action")
