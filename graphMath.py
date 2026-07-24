import basketList
import matplotlib.pyplot as plt

# basket = basketList.saved_basket
basket = basketList.basket

maxprofit = -1
maxloss = -1
breakeven = -1

lots = 65

currentStrike = 24350
totalCost = 0

def callsPuts():
    global maxprofit, maxloss, breakeven, lots, currentStrike, totalCost, basket

    totalCost = 0
    calls = []
    puts = []
    for i in range(len(basket)):
        totalCost += float(basket[i][0])

        if basket[i][4] == "CALL":
            calls.append([basket[i][1], basket[i][3]])
        elif basket[i][4] == "PUT":
            puts.append([basket[i][1], basket[i][3]])

    calls.sort(key=lambda item: float(item[0]))
    puts.sort(key=lambda item: float(item[0]))

    return calls, puts, totalCost

if basket:
    print("Total Cost: ", totalCost, basket)
    print("Type: ", basket[0][4], basket[0][3])

    if basket[0][4] == "CALL":
        maxprofit = float('inf')
        breakeven = int(float(basket[0][1])) + totalCost

print(f"Max Profit: {maxprofit}, Max Loss: {maxloss}, Breakeven: {breakeven}")

def drawGraph(ax, canvas):
    global maxprofit, maxloss, breakeven, lots, currentStrike, totalCost, basket

    # x_coords = [23000, 23500, 24000, 24500, 25000]
    # y_coords = [2000, -1500, -3000, -1500, 5000]
    x_coords = []
    y_coords = []
    calls, puts, totalCost = callsPuts()

    maxloss = -totalCost

    for i in range(len(calls)):
        x_coords.append(float(calls[i][0]))

        if y_coords == []:
            y_coords.append(maxloss)
        else:
            y_coords.append(y_coords[-1] + ((x_coords[-1] - x_coords[-2]) * i))

    y_coords = [round(y, 2) for y in y_coords]

    x_coords.append(190)
    y_coords.append(y_coords[-1] + ((x_coords[-1] - x_coords[-2]) * (len(x_coords) - 1)))

    print(f"x:{x_coords}")
    print(f"y:{y_coords}")

    while len(ax.lines) > 2:
        ax.lines[-1].remove()
    ax.plot(x_coords, y_coords, color = "#C300FF", linewidth = 2)
    
    canvas.draw()
    