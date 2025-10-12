def validate_information(name: str, address: str) -> str:
    """Make sure to validate the name and address of a person
    Args:
        name (str): Name of person
        address (str): Address of person

    Returns:
        info: Name first, then address
    
    Raises:
        ValueError: If name and address are empty strings

    Examples:
        >>> validate_information("Tim  ,  Cook", "23 Candy Lane")
        'Tim Cook - 23 Candy Lane'
        >>> validate_information("Adam", "421  Happy Lane")
        'Adam - 421 Happy Lane'
    """
    if name == "" or address == "":
          raise ValueError("Name and address have to be a non-empty string.")
    
    clean_name = ' '.join(name.replace(',', ' ').split())
    clean_address = ' '.join(address.replace('  ', ' ').split())

    info = f"{clean_name} - {clean_address}"
    return info


def format_query(name: str, age: int, country: str) -> str:
    """Formats the query to show the name, age, and country of a person
    Args:
        name (str): Name of person
        age (int): Age of person
        country (str): Country of origin
    
    Returns:
        format: formatted string that prints out name, then age, and country in parentheses

    Examples:
        >>> format_query(" Bonnie  ", 28, "United States")
        'Bonnie, 28 (United States)'
        >>> format_query("    Eva   ", 30, "Iceland")
        'Eva, 30 (Iceland)'
    """
    name = name.strip()
    country = country.strip()

    format = f"{name}, {age} ({country})"
    return format

def calculate_user_distance(distance1: int, distance2: int) -> int:
    """Calculates distance between two points
    Args:
        distance1 (int): First distance number
        distance2 (int): Second distance number
    
    Returns:
        Difference between the first distance and the second distance
    
    Raises:
        ValueErrors if both distances are less than 0.
    
    Examples:
        >>> calculate_user_distance(200, 150)
        50 km
        >>> calculate_user_distance(300, 150)
        150 km
    """
    # value error for distance 1
    if distance1 < 0:
        raise ValueError("Distance 1 must be greater than 0.")
    
    
    # value error for distance 2
    if distance2 < 0:
        raise ValueError("Distance 2 must be greater than 0.")
    

    # Finds the difference by subtracting the first distance and the second distance
    distance_difference = distance1 - distance2


    # returns distance in kilometers
    return f"{distance_difference} km"

def parse_user_order(food_items: list[str], user_order: str) -> str:
    """Goes through user order and picks out
    Args:
        food_items: List of foods that are available on the menu
        user_order (str): Order the user has
    
    Returns:
        food_order = complete order for the person

    Raises:
        ValueError: if item is not on the list

    Examples:
        >>> parse_user_order(['sushi', 'ice cream', 'fish'], 'sushi', 'ice cream')
            'sushi', 'ice cream'
        >>> parse_user_order(['sushi', 'ice cream', 'fish', 'burger'], 'burger')
            'burger'
        """

    #Separates the items with a comma, makes it easier to know what the person ordered
    split_items = user_order.split(',')

    #Empty list 
    parse = []

    for item in split_items:
        cleaned_item = item.strip()
    
        if cleaned_item not in parse:
            raise ValueError("Food item has to be on order list.")
        
        parse.append(cleaned_item)

    food_order = ", ".join(parse)
    return f"{food_order}"

def process_multiple_order_data(order_data: list[str]) -> str:
    """Processes order data from multiple people 
    Args:
        order_data: List of strings consisting of name, food item and amount

    Returns:
        multiple_orders: Shows name, followed by number of food, and the food item for 
        each person.
    
    Raises:
        ValueError: Happens if the length of orders is less than 3 and if
        quantity of food is less than 0 or greater than 5.
    
    Examples:
        >>> order_data = ["Adrian, cheeseburger, 2", "Bob, snack wrap, 2", "Cory, pizza, 1"]
            process_multiple_order_data(order_data)
            Adrian: 3 cheeseburgers
            Bob: 2 snack wraps
            Cory: 1 pizza
        >>> order_data = ["Gary, chicken sandwich, 2", "Joe, pasta, 1", "Sarah, cake, 2"]
            process_multiple_order_data(order_data)
            Gary: 2 chicken sandwiches
            Joe: 1 pasta
            Sarah: 2 cakes
        """
    if len(order_data) < 3:
        raise ValueError("length of order data has to be 3")
    
    all_orders = []

    # for loop that goes through each part of the order
    for order in order_data:
        parts_of_order = order.split(',')

        person = parts_of_order[0].strip()
        food_item = parts_of_order[1].strip()
        amount_food = parts_of_order[2].strip()


        if amount_food < 0 or amount_food > 5:
            raise ValueError("Amount of food wanted has to be greater than 0.")
        
        # adds only one item to the order
        if amount_food == 1:
            return f"{person}: 1 {food_item}" 

        if amount_food == 2: 
            return f"{person}: 2 {food_item}" 

        if amount_food == 3:
            return '3' + food_item + 's'
        
        if amount_food == 4:
            return '4' + food_item + 's'

        if amount_food == 5:
            return '5' + food_item + 's'
    
    order_description = f"{person}: {amount_food} {food_item}"
    all_orders.append(order_description)
    return f"{all_orders}"

print(validate_information("Seth Curry,", "31 Basketball Avenue"))
print(format_query("Kevin James", 35, "United States"))
print(calculate_user_distance(50, 20))

food_items = ['cheeseburger', 'gyros', 'fries', 'pizza', 'cheeseburger, gyros']
print(parse_user_order(food_items))

order_data = ["Jeff, cheeseburger, 3", "Bob, snack wrap, 1", "Cory, pizza, 2"]
print(process_multiple_order_data(order_data))