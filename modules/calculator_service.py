#!/usr/bin/env python3
"""
Calculator and Unit Conversion Service
Handles mathematical calculations and unit conversions
"""

import re
import math
from typing import Optional, Dict, Any

class CalculatorService:
    def __init__(self):
        """Initialize calculator service"""
        # Unit conversion factors (to base units)
        self.conversions = {
            # Length (to meters)
            'length': {
                'mm': 0.001, 'millimeter': 0.001, 'millimeters': 0.001, 'millimetre': 0.001, 'millimetres': 0.001,
                'cm': 0.01, 'centimeter': 0.01, 'centimeters': 0.01, 'centimetre': 0.01, 'centimetres': 0.01,
                'm': 1.0, 'meter': 1.0, 'meters': 1.0, 'metre': 1.0, 'metres': 1.0,
                'km': 1000.0, 'kilometer': 1000.0, 'kilometers': 1000.0, 'kilometre': 1000.0, 'kilometres': 1000.0,
                'in': 0.0254, 'inch': 0.0254, 'inches': 0.0254,
                'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
                'yd': 0.9144, 'yard': 0.9144, 'yards': 0.9144,
                'mi': 1609.34, 'mile': 1609.34, 'miles': 1609.34
            },
            # Weight (to grams)
            'weight': {
                'mg': 0.001, 'milligram': 0.001, 'milligrams': 0.001,
                'g': 1.0, 'gram': 1.0, 'grams': 1.0,
                'kg': 1000.0, 'kilogram': 1000.0, 'kilograms': 1000.0,
                'oz': 28.3495, 'ounce': 28.3495, 'ounces': 28.3495,
                'lb': 453.592, 'pound': 453.592, 'pounds': 453.592,
                'ton': 1000000.0, 'tons': 1000000.0, 'tonne': 1000000.0, 'tonnes': 1000000.0
            },
            # Temperature (special handling)
            'temperature': {
                'c': 'celsius', 'celsius': 'celsius',
                'f': 'fahrenheit', 'fahrenheit': 'fahrenheit',
                'k': 'kelvin', 'kelvin': 'kelvin'
            },
            # Volume (to liters)
            'volume': {
                'ml': 0.001, 'milliliter': 0.001, 'milliliters': 0.001,
                'l': 1.0, 'liter': 1.0, 'liters': 1.0, 'litre': 1.0, 'litres': 1.0,
                'gal': 3.78541, 'gallon': 3.78541, 'gallons': 3.78541,
                'qt': 0.946353, 'quart': 0.946353, 'quarts': 0.946353,
                'pt': 0.473176, 'pint': 0.473176, 'pints': 0.473176,
                'cup': 0.236588, 'cups': 0.236588,
                'fl oz': 0.0295735, 'fluid ounce': 0.0295735, 'fluid ounces': 0.0295735
            }
        }
    
    def calculate(self, expression: str) -> str:
        """
        Perform mathematical calculation
        
        Args:
            expression: Mathematical expression
            
        Returns:
            str: Result description
        """
        try:
            # Clean the expression
            expression = expression.lower().strip()
            
            # Handle special math functions
            expression = self._handle_math_functions(expression)
            
            # Replace common words with operators
            replacements = {
                'plus': '+', 'add': '+', 'added to': '+',
                'minus': '-', 'subtract': '-', 'take away': '-',
                'times': '*', 'multiply': '*', 'multiplied by': '*',
                'divide': '/', 'divided by': '/', 'over': '/',
                'to the power of': '**', 'raised to': '**', 'squared': '**2',
                'cubed': '**3', 'square root of': 'sqrt(',
                'percent': '/100', 'percentage': '/100'
            }
            
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Handle square root
            if 'sqrt(' in expression and not expression.count('sqrt(') == expression.count(')'):
                expression = expression.replace('sqrt(', 'sqrt(') + ')'
            
            # Remove non-mathematical characters (keep numbers, operators, parentheses, and math functions)
            expression = re.sub(r'[^0-9+\-*/().sqrt()pow()sin()cos()tan()log()ln()pi()e]', '', expression)
            
            # Replace math constants
            expression = expression.replace('pi', str(math.pi))
            expression = expression.replace('e', str(math.e))
            
            # Evaluate the expression safely
            result = self._safe_eval(expression)
            
            if result is not None:
                # Format the result nicely
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 6)
                
                return f"The answer is {result}"
            else:
                return "I couldn't calculate that expression. Please check the format."
                
        except Exception as e:
            print(f"Calculation error: {e}")
            return "I couldn't perform that calculation. Please try a simpler expression."
    
    def _handle_math_functions(self, expression: str) -> str:
        """Handle mathematical functions"""
        # Replace function names
        functions = {
            'sine': 'sin', 'cosine': 'cos', 'tangent': 'tan',
            'logarithm': 'log', 'natural log': 'log', 'ln': 'log'
        }
        
        for func_name, func_symbol in functions.items():
            expression = expression.replace(func_name, func_symbol)
        
        return expression
    
    def _safe_eval(self, expression: str) -> Optional[float]:
        """Safely evaluate mathematical expression"""
        try:
            # Define safe functions
            safe_dict = {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log10,
                'ln': math.log,
                'pow': pow,
                'abs': abs,
                'round': round,
                'pi': math.pi,
                'e': math.e
            }
            
            # Use eval with restricted namespace
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return float(result)
            
        except Exception:
            return None
    
    def convert_units(self, amount: float, from_unit: str, to_unit: str) -> str:
        """
        Convert between units
        
        Args:
            amount: Amount to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            str: Conversion result
        """
        try:
            from_unit = from_unit.lower().strip()
            to_unit = to_unit.lower().strip()
            
            # Find which category the units belong to
            from_category = None
            to_category = None
            
            for category, units in self.conversions.items():
                if from_unit in units:
                    from_category = category
                if to_unit in units:
                    to_category = category
            
            if not from_category or not to_category:
                return f"I don't recognize one of those units. I can convert length, weight, volume, and temperature."
            
            if from_category != to_category:
                return f"I can't convert between {from_category} and {to_category} units."
            
            # Handle temperature conversion separately
            if from_category == 'temperature':
                result = self._convert_temperature(amount, from_unit, to_unit)
            else:
                # Convert to base unit, then to target unit
                base_amount = amount * self.conversions[from_category][from_unit]
                result = base_amount / self.conversions[to_category][to_unit]
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 4)
            
            return f"{amount} {from_unit} equals {result} {to_unit}"
            
        except Exception as e:
            print(f"Conversion error: {e}")
            return "I couldn't perform that conversion. Please check the units."
    
    def _convert_temperature(self, amount: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature units"""
        from_unit = self.conversions['temperature'][from_unit]
        to_unit = self.conversions['temperature'][to_unit]
        
        # Convert to Celsius first
        if from_unit == 'fahrenheit':
            celsius = (amount - 32) * 5/9
        elif from_unit == 'kelvin':
            celsius = amount - 273.15
        else:  # celsius
            celsius = amount
        
        # Convert from Celsius to target
        if to_unit == 'fahrenheit':
            return celsius * 9/5 + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
        else:  # celsius
            return celsius
    
    def get_math_help(self) -> str:
        """Get help text for math operations"""
        help_text = """I can help with calculations and unit conversions. Examples:
        
        Math: "Calculate 15 plus 25", "What's 12 times 8", "Square root of 144"
        
        Conversions: "Convert 5 feet to meters", "How many pounds in 10 kilograms"
        
        I support: length, weight, volume, and temperature conversions."""
        
        return help_text

# Test function
def test_calculator_service():
    """Test the calculator service"""
    print("Testing Calculator Service")
    print("=" * 30)
    
    calc = CalculatorService()
    
    # Test calculations
    print("1. Basic calculations:")
    print(f"   15 + 25: {calc.calculate('15 plus 25')}")
    print(f"   12 * 8: {calc.calculate('12 times 8')}")
    print(f"   sqrt(144): {calc.calculate('square root of 144')}")
    
    # Test conversions
    print("\n2. Unit conversions:")
    print(f"   5 ft to m: {calc.convert_units(5, 'feet', 'meters')}")
    print(f"   10 kg to lb: {calc.convert_units(10, 'kilograms', 'pounds')}")
    print(f"   32 F to C: {calc.convert_units(32, 'fahrenheit', 'celsius')}")

if __name__ == "__main__":
    test_calculator_service()