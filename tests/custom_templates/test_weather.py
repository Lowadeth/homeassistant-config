import pytest
from jinja2 import Environment, FileSystemLoader
import yaml
import os
from datetime import datetime, timezone

def test_has_rain_macro():
    """Test the has_rain macro."""
    # Setup Jinja2 environment with whitespace control
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../usr/share/hassio/homeassistant')),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Get the template
    template = env.get_template('custom_templates/weather.jinja')
    
    # Test with rain in forecast
    test_data_with_rain = [
        {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 1.5},
        {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
    ]
    result_with_rain = template.module.has_rain(test_data_with_rain).strip()
    assert result_with_rain == "true"

    # Test without rain in forecast
    test_data_without_rain = [
        {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
    ]
    result_without_rain = template.module.has_rain(test_data_without_rain).strip()
    assert result_without_rain == "false"

    # Test with no-rain-minutes.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'no-rain-minutes.yaml'), 'r') as file:
        no_rain_data = yaml.safe_load(file)
        # Extract forecast data from the YAML file
        forecast_data = no_rain_data['weather.openweathermap']['forecast']
        result_no_rain_data = template.module.has_rain(forecast_data).strip()
        assert result_no_rain_data == "false"

def test_minutes_until_rain_macro():
    """Test the minutes_until_rain macro."""
    # Setup Jinja2 environment with whitespace control
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../usr/share/hassio/homeassistant')),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Get the template
    template = env.get_template('custom_templates/weather.jinja')
    
    # Test with rain in forecast
    test_data_with_rain = [
        {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 1.5},
        {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
    ]
    result_with_rain = template.module.minutes_until_rain(test_data_with_rain).strip()
    assert result_with_rain == "1"  # 1 minute until rain starts

    # Test without rain in forecast
    test_data_without_rain = [
        {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
    ]
    result_without_rain = template.module.minutes_until_rain(test_data_without_rain).strip()
    assert result_without_rain == "no_rain"

    # Test with its-raining-in-minutes.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'its-raining-in-minutes.yaml'), 'r') as file:
        rain_data = yaml.safe_load(file)
        # Extract forecast data from the YAML file
        forecast_data = rain_data['weather.openweathermap']['forecast']
        result_rain_data = template.module.minutes_until_rain(forecast_data).strip()
        # The first rain is at 17:13, so we expect 28 minutes from 16:45
        assert result_rain_data == "28" 