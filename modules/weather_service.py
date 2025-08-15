#!/usr/bin/env python3
"""
Weather Service Module
Fetches weather information from online APIs
"""

import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime

class WeatherService:
    def __init__(self):
        """Initialize weather service"""
        # Using OpenWeatherMap free API (requires API key)
        # For demo purposes, we'll use a free weather API that doesn't require key
        self.apis = [
            {
                'name': 'wttr.in',
                'base_url': 'https://wttr.in',
                'parser': self._parse_wttr
            }
        ]
        
    def get_weather(self, location: str = None) -> str:
        """
        Get current weather for location
        
        Args:
            location: Location name (defaults to auto-detect)
            
        Returns:
            str: Weather description
        """
        if not location:
            location = ""  # wttr.in auto-detects location
        
        try:
            # Try wttr.in API
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_wttr(data, location or "your location")
            else:
                return self._get_fallback_weather()
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_fallback_weather()
    
    def _parse_wttr(self, data: Dict[str, Any], location: str) -> str:
        """Parse wttr.in API response"""
        try:
            current = data['current_condition'][0]
            
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            feels_like_c = current['FeelsLikeC']
            feels_like_f = current['FeelsLikeF']
            
            # Get location info
            location_info = data.get('nearest_area', [{}])[0]
            area_name = location_info.get('areaName', [{'value': location}])[0]['value']
            country = location_info.get('country', [{'value': ''}])[0]['value']
            
            location_str = f"{area_name}, {country}" if country else area_name
            
            weather_report = f"Current weather in {location_str}: "
            weather_report += f"{desc}, {temp_c}°C or {temp_f}°F. "
            weather_report += f"Feels like {feels_like_c}°C or {feels_like_f}°F. "
            weather_report += f"Humidity {humidity}%, "
            weather_report += f"wind {wind_speed} km/h from the {wind_dir}."
            
            return weather_report
            
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return self._get_fallback_weather()
    
    def get_forecast(self, location: str = None, days: int = 3) -> str:
        """
        Get weather forecast
        
        Args:
            location: Location name
            days: Number of days (1-3)
            
        Returns:
            str: Forecast description
        """
        if not location:
            location = ""
        
        try:
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_forecast(data, location or "your location", days)
            else:
                return "I'm unable to get the weather forecast right now."
                
        except Exception as e:
            print(f"Forecast API error: {e}")
            return "I'm unable to get the weather forecast right now."
    
    def _parse_forecast(self, data: Dict[str, Any], location: str, days: int) -> str:
        """Parse forecast data"""
        try:
            weather_data = data.get('weather', [])
            if not weather_data:
                return "No forecast data available."
            
            location_info = data.get('nearest_area', [{}])[0]
            area_name = location_info.get('areaName', [{'value': location}])[0]['value']
            
            forecast_text = f"Weather forecast for {area_name}: "
            
            for i, day_data in enumerate(weather_data[:days]):
                date = day_data['date']
                max_temp_c = day_data['maxtempC']
                min_temp_c = day_data['mintempC']
                max_temp_f = day_data['maxtempF']
                min_temp_f = day_data['mintempF']
                
                # Get main weather description
                hourly = day_data.get('hourly', [{}])
                if hourly:
                    desc = hourly[0].get('weatherDesc', [{'value': 'Unknown'}])[0]['value']
                else:
                    desc = "Unknown"
                
                # Format date
                try:
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    day_name = date_obj.strftime('%A')
                except:
                    day_name = f"Day {i+1}"
                
                if i == 0:
                    day_name = "Today"
                elif i == 1:
                    day_name = "Tomorrow"
                
                forecast_text += f"{day_name}: {desc}, "
                forecast_text += f"high {max_temp_c}°C ({max_temp_f}°F), "
                forecast_text += f"low {min_temp_c}°C ({min_temp_f}°F). "
            
            return forecast_text
            
        except Exception as e:
            print(f"Error parsing forecast: {e}")
            return "Unable to parse forecast data."
    
    def _get_fallback_weather(self) -> str:
        """Fallback weather response"""
        return "I'm unable to get the current weather information. Please check your internet connection and try again."

# Test function
def test_weather_service():
    """Test the weather service"""
    print("Testing Weather Service")
    print("=" * 30)
    
    service = WeatherService()
    
    print("1. Current weather (auto-location):")
    weather = service.get_weather()
    print(f"   {weather}")
    
    print("\n2. Weather for specific location:")
    weather_london = service.get_weather("London")
    print(f"   {weather_london}")
    
    print("\n3. Weather forecast:")
    forecast = service.get_forecast("", 2)
    print(f"   {forecast}")

if __name__ == "__main__":
    test_weather_service()