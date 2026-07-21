import json

basket = []

def clearBasket():
    global basket
    basket = []

def saveBasket(filename="saved_basket.json"):
    try:
        with open(filename, "w") as f:
            json.dump(basket, f, indent = 4)
    except Exception as e:
        print(f"Error saving basket: {e}")

    print(f"Basket saved to {filename}")
