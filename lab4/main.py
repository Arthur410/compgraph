import turtle

def create_l_system(iters, axiom, rules):
    start_string = axiom
    if iters == 0:
        return axiom
    end_string = ""
    for _ in range(iters):
        end_string = "".join(rules[i] if i in rules else i for i in start_string)
        start_string = end_string

    return end_string

def draw_l_system(t, instructions, angle, distance):
    for cmd in instructions:
        if cmd == 'F':
            t.forward(distance)
        elif cmd == '-':
            t.right(angle)
        elif cmd == '+':
            t.left(angle)

def main(iterations, axiom, rules, angle, length=8, size=2, y_offset=0,
        x_offset=0, offset_angle=0, width=450, height=450):

    inst = create_l_system(iterations, axiom, rules)

    t = turtle.Turtle()
    wn = turtle.Screen()
    wn.setup(width, height)

    # Настройка положения черепашки в центре экрана
    t.up()
    t.goto(-150, -150)  # Центр экрана
    t.down()

    t.speed(0)
    t.pensize(size)
    draw_l_system(t, inst, angle, length)
    t.hideturtle()

    wn.exitonclick()

def recursive_string(string, iterations):
    prev_string = string
    result = string

    for _ in range(iterations):
        if _ % 2 == 0:
            new_string = prev_string.replace('+', 'temp').replace('-', '+').replace('temp', '-')
            result = f'+{new_string}-F-{new_string}'
        else:
            new_string = prev_string.replace('+', 'temp').replace('-', '+').replace('temp', '-')
            if new_string[0] == '-':
                new_string = new_string[1:]
            result = f'{new_string}--F--{new_string}'

        prev_string = result

    return result

# Пример использования:
initial_string = "F"
num_iterations = 8
real_iterations = num_iterations - 1;
result = recursive_string(initial_string, real_iterations)
print(result)

axiom = "F"
rules = {"F": result}
iterations = 1
angle = 45

main(iterations, axiom, rules, angle)