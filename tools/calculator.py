def calculate_macros(protein: float, carbs: float, fat: float) -> dict:
    """
    Calculates the total calories based on macronutrients.
    
    Args:
        protein: Grams of protein.
        carbs: Grams of carbohydrates.
        fat: Grams of fat.
        
    Returns:
        A dictionary containing the input macros and total calories.
    """
    calories = (protein * 4) + (carbs * 4) + (fat * 9)
    return {
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "total_calories": calories
    }
