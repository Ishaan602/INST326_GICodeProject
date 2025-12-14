# Completed by Zachery Tong 

class UserProfile:
    """Represents a profile from a user in an infomation retrieval system.

    This class encapsulates user profile data and provides methods for validating information, 
    calculating user distance, parsing a user order, formatting a query, and processing multiple
    orders.
    
    Attributes:
        __name (str): Name of a person
        __address (str): Address of a person
        __age (str): Age of a person
        __country (str): Country of origin
        __distance1 (int): First distance
        __distance2 (int): Second distance
        __food_items (list): All items in the user's order
        __order_data (list): Shows name of person, food item and amount of food
        __user_order (str): Information of the order that the user has
    
    Examples:
        >>> new_user1 = UserProfile("Seth Curry", "31 Basketball Avenue", 35, "United States",
                                    4, 2, ['sushi', 'burger', 'chicken sandwich'], 
                                    ["Seth, burger, 1", "Bob, snack wrap, 2", "Mark, pizza, 1"],
                                    "Burger: 1, Chicken Sandwich: 2")
        >>> new_user1.name
            'Seth Curry'
        >>> new_user2 = UserProfile("Shohei Ohtani", "103 Baseball Lane", 31, "Japan",
                                    3, 1, ['steak', 'pasta', 'fish'],
                                    ["Shohei, pasta, 3", "Devon, cake, 2", "Jim, shrimp, 1"],
                                    "Steak: 1, Pasta: 3")
        >>> new_user2.age
            31
    """

    def __init__(self, name: str, address: str, age: int, country: str, distance1: int, distance2: int, food_items: list[str], order_data: list[str], user_order: str):
        """Initializes an instance of a User.

        Args:
            name (str): Name of a person
            address (str): Address of a person
            age (int): Age of a person
            country (str): Country where person is from
            distance1 (int): First distance for the user
            distance2 (int): Second distance for the user
            food_items (list): All items in the order
            order_data (list): Information of specific order characteristics of multiple people
            user_order (str): Information of the eorder that the user has

        Raises:
            ValueError: If name string is empty, or age or distance is less than 0.
            TypeError: If every argument is not the correct type

        Examples:
            >>> new_user1 = UserProfile("Jayson Tatum", "115 Celtics Avenue", 27, "United States",
                                    6, 3, ['fries', 'ice cream', 'salad'], 
                                    ["Jayson, salad, 2", "Kendrick, chicken, 1", "Charlie, donuts, 2"]
                                    "Ice Cream: 3, Salad: 2")
            >>> new_user1.country
            'United States'
            >>> new_user2 = UserProfile("Alan Turing", "264 Code Lane", 40, "Germany",
                                    2, 1, ['pasta', 'ice cream', 'fish'], 
                                    ["Alan, pasta, 3", "Bill, tacos, 2", "Sam, hot dog, 2"]
                                    "Steak: 1, Pasta: 3")
            >>> new_user2.address
            '264 Code Lane'
    
        """
        self.__name = name
        self.__address = address
        self.__age = age
        self.__country = country
        self.__distance1 = distance1
        self.__distance2 = distance2
        self.__food_items = food_items
        self.__order_data = order_data
        self.__user_order = user_order

        # Parameter validation
        if not isinstance(name, str):
            raise TypeError("name has to be a string.")
        
        if not isinstance(address, str):
            raise TypeError("address has to be a string.")
        
        if not isinstance(age, int):
            raise TypeError("age has to be a number.")
        
        if not isinstance(country, str):
            raise TypeError("country has to be a string.")
        
        if not isinstance(distance1, int):
            raise TypeError("distance1 has to be a number.")
        
        if not isinstance(distance2, int):
            raise TypeError("distance2 has to be a number.")
        
        if not isinstance(food_items, list):
            raise TypeError("food_items has to be a list.")
        
        if not isinstance(order_data, list):
            raise TypeError("food_items has to be a list.")

        if not isinstance(user_order, str):
            raise TypeError("user_order has to be a string.")

        if not name.strip():
            raise ValueError("name has to be a non-empty string.")
        
        if not address.strip():
            raise ValueError("address has to be a non-empty string.")
        
        if age < 0:
            raise ValueError("age has to be greater than 0.")

        if distance1 < 0:
            raise ValueError("distance has to be greater than 0.")
        
        if distance2 < 0:
            raise ValueError("distance has to be greater than 0.")
        

    @property
    def name(self) -> str:
        """Gets the name of the person.

        Returns:
            str: name of person
        """
        return self.__name
    
    @property
    def address(self) -> str:
        """Gets the address of the person.

        Returns:
            str: address of person
        """
        return self.__address
    
    @property
    def age(self) -> str:
        """Gets the age of the person.

        Returns:
            str: age of person
        """
        return self.__age
    
    @property
    def country(self) -> str:
        """Gets the country of origin for the person.

        Returns:
            str: country of origin
        """
        return self.__country
    
    @property
    def distance1(self) -> int:
        """Gets the first distance of the person.

        Returns:
            int: first distance of person
        """
        return self.__distance1
    
    @property
    def distance2(self) -> int:
        """Gets the second distance of the person.

        Returns:
            int: second distance of person
        """
        return self.__distance2
    
    @property
    def food_items(self) -> list[str]:
        """Gets the list of food items.

        Returns:
            list[str]: list of food items
        """
        return self.__food_items
    
    @property
    def order_data(self) -> list[str]:
        """Gets the list of order information

        Returns:
            list[str]: list of order information
        """
        return self.__order_dara
    
    @property
    def user_order(self) -> str:
        """Gets the order of the person.

        Returns:
            str: order that the user has
        """
        return self.__user_order

    
def validate(self, name: str, address: str) -> str:
    """Make sure to validate the name and address of a person

    Integrates the validate_information() function to make sure
    the information provided is valid.

    Args:
        name (str): Name of person
        address (str): Address of person

    Returns:
        str: Name and address
    
    Raises:
        ValueError: If name and address are empty strings

    Examples:
        >>> profile = UserProfile("Tim  ,  Cook", "23 Candy Lane")
        >>> profile.validate()
        'Tim Cook - 23 Candy Lane'
        >>> profile = UserProfile("Adam", "421  Happy Lane")
        >>> profile.validate()
        'Adam - 421 Happy Lane'
    """
    if name == "" or address == "":
          raise ValueError("Name and address have to be a non-empty string.")
    
    clean_name = ' '.join(self.__name.replace(',', ' ').split())
    clean_address = ' '.join(self.__address.replace('  ', ' ').split())

    info = f"{clean_name} - {clean_address}"
    return info


def format(self, name: str, age: int, country: str) -> str:
    """Formats the query to show the name, age, and country of a person

    Integrates the format_query() function to create a query that is
    formatted properly.

    Args:
        name (str): Name of person
        age (int): Age of person
        country (str): Country of origin
    
    Returns:
        format: formatted string that prints out name, then age, and country in parentheses

    Examples:
        >>> profile = UserProfile(" Bonnie  ", 28, "United States")
        >>> profile.format_query()
        'Bonnie, 28 (United States)'
        >>> profile = UserProfile("    Eva   ", 30, "Iceland")
        >>> profile.format_query()
        'Eva, 30 (Iceland)'
        
    """
    name = self.__name.strip()
    country = self.__country.strip()

    format = f"{name}, {age} ({country})"
    return format

def user_distance(self, distance1: int, distance2: int) -> int:
    """Calculates distance between two points

    Integrates the calculate_user_distance() function to subtract
    second distance from first distance.

    Args:
        distance1 (int): First distance number
        distance2 (int): Second distance number
    
    Returns:
        int: Difference between the first distance and the second distance
    
    Raises:
        ValueErrors if both distances are less than 0.
    
    Examples:
        >>> profile = UserProfile(200, 150)
        >>> profile.calculate_user_distance()
        50 km
    """
    # value error for distance 1
    if self.__distance1 < 0:
        raise ValueError("Distance 1 must be greater than 0.")
    
    
    # value error for distance 2
    if self.__distance2 < 0:
        raise ValueError("Distance 2 must be greater than 0.")
    

    # Finds the difference by subtracting the first distance and the second distance
    distance_difference = self.__distance1 - self.__distance2


    # returns distance in kilometers
    return f"{distance_difference} km"

def user_order(self, food_items: list[str], user_order: str) -> str:
    """Goes through user order and picks out

    Integrates the parse_user_order() function to make sure
    the food items is on the order list.

    Args:
        food_items: List of foods that are available on the menu
        user_order (str): Order the user has
    
    Returns:
        str: food items that are in the list

    Raises:
        ValueError: if item is not on the list

    Examples:
        >>> profile = UserProfile(['sushi', 'ice cream', 'fish'], 'sushi', 'ice cream')
        >>> profile.user_order()
            'sushi', 'ice cream'
        """

    #Separates the items with a comma, makes it easier to know what the person ordered
    split_items = self.__user_order.split(',')

    #Empty list 
    parse = []

    for item in split_items:
        cleaned_item = item.strip()
    
        if cleaned_item not in parse:
            raise ValueError("Food item has to be on order list.")
        
        parse.append(cleaned_item)

    food_order = ", ".join(parse)
    return f"{food_order}"

def process_multiple_orders(self, order_data: list[str]) -> str:
    """Processes order data from multiple people 

    Integrates the process_multiple_order_data() function to make sure
    that every order from every person is processed and printed.

    Args:
        order_data: List of strings consisting of name, food item and amount

    Returns:
        str: shows name, amount of food person got, and food item
    
    Raises:
        ValueError: Happens if the length of orders is less than 3 and if
        quantity of food is less than 0 or greater than 5.
    
    Examples:
        >>> profile = UserProfile(["Adrian, cheeseburger, 2", "Bob, snack wrap, 2", "Cory, pizza, 1"])
        >>> profile.process_multiple_orders()
            Adrian: 3 cheeseburgers
            Bob: 2 snack wraps
            Cory: 1 pizza
        """
    if len(self.__order_data) < 3:
        raise ValueError("length of order data has to be 3")
    
    all_orders = []

    # for loop that goes through each part of the order
    for order in self.__order_data:
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


def __str__(self) -> str:
        """Return a human-readable string representation of the user profile.

        Returns:
            str: Formatted string showing normalized profile and term count
            
        Examples:
            >>> profile = UserProfile("Giannis Antetokounmpo", "34 Greek Avenue", 30, "Greece",
                                    8, "Gyros: 1, Souvlaki: 2")
            >>> str(profile)
            'Profile: "Giannis Antetokounmpo"'
        """
        return f"Profile: {self.__name}"

    
def __repr__(self) -> str:
        """Return a detailed string representation for debugging.
        
        Returns:
            str: Detailed representation with every key attribute
            
        Examples:
            >>> profile = UserProfile("Ben Franklin", "20 Money Drive", 60, "United States",
                                    11, "Fish: 2, Steak: 1")
            >>> repr(profile)
            'UserProfile(name="Ben Franklin", address="20 Money Drive", age="60",
                                    country="United States", distance=11, order="Fish: 2, Steak: 1")'  
        """
        return f"UserProfile(name={self.__name}, address={self.__address}, age={self.__age}, country={self.__country}, distance={self.__distance}, order={self.__user_order})"

    

