import pytest
from jinja2 import Environment, FileSystemLoader
import yaml
import os
import json
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
    result_with_rain = json.loads(template.module.minutes_until_rain(test_data_with_rain).strip())
    assert result_with_rain['time'] == '2025-06-09T17:46:00+00:00'
    assert result_with_rain['resolution'] == 'minutes'

    # Test without rain in forecast
    test_data_without_rain = [
        {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
    ]
    result_without_rain = json.loads(template.module.minutes_until_rain(test_data_without_rain).strip())
    assert result_without_rain['time'] == 'no_rain'
    assert result_without_rain['resolution'] == 'minutes'

    # Test with its-raining-in-minutes.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'its-raining-in-minutes.yaml'), 'r') as file:
        rain_data = yaml.safe_load(file)
        # Extract forecast data from the YAML file
        forecast_data = rain_data['weather.openweathermap']['forecast']
        result_rain_data = json.loads(template.module.minutes_until_rain(forecast_data).strip())
        assert result_rain_data['time'] == '2025-06-10T17:13:00+00:00'
        assert result_rain_data['resolution'] == 'minutes'

def test_hours_until_rain_macro():
    """Test the hours_until_rain macro."""
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
        {'datetime': '2025-06-10T17:00:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-10T18:00:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-10T19:00:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-10T20:00:00+00:00', 'precipitation': 0.4}
    ]
    result_with_rain = json.loads(template.module.hours_until_rain(test_data_with_rain).strip())
    assert result_with_rain['time'] == '2025-06-10T20:00:00+00:00'
    assert result_with_rain['resolution'] == 'hours'

    # Test without rain in forecast
    test_data_without_rain = [
        {'datetime': '2025-06-10T17:00:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-10T18:00:00+00:00', 'precipitation': 0},
        {'datetime': '2025-06-10T19:00:00+00:00', 'precipitation': 0}
    ]
    result_without_rain = json.loads(template.module.hours_until_rain(test_data_without_rain).strip())
    assert result_without_rain['time'] == 'no_rain'
    assert result_without_rain['resolution'] == 'hours'

    # Test with its-raining-in-hours.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'its-raining-in-hours.yaml'), 'r') as file:
        rain_data = yaml.safe_load(file)
        # Extract forecast data from the YAML file
        forecast_data = rain_data['weather.openweathermap']['forecast']
        result_rain_data = json.loads(template.module.hours_until_rain(forecast_data).strip())
        assert result_rain_data['time'] == '2025-06-10T20:00:00+00:00'
        assert result_rain_data['resolution'] == 'hours'

def test_days_until_no_rain_macro():
    """Test the days_until_no_rain macro."""
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
        {'datetime': '2025-06-10T11:00:00+00:00', 'precipitation': 8.66},
        {'datetime': '2025-06-11T11:00:00+00:00', 'precipitation': 4.0},
        {'datetime': '2025-06-12T11:00:00+00:00', 'precipitation': 0}
    ]
    result_with_rain = json.loads(template.module.days_until_no_rain(test_data_with_rain).strip())
    assert result_with_rain['time'] == '2025-06-12T11:00:00+00:00'
    assert result_with_rain['resolution'] == 'days'

    # Test with always rain in forecast
    test_data_always_rain = [
        {'datetime': '2025-06-10T11:00:00+00:00', 'precipitation': 8.66},
        {'datetime': '2025-06-11T11:00:00+00:00', 'precipitation': 4.0},
        {'datetime': '2025-06-12T11:00:00+00:00', 'precipitation': 2.0}
    ]
    result_always_rain = json.loads(template.module.days_until_no_rain(test_data_always_rain).strip())
    assert result_always_rain['time'] == 'always_rain'
    assert result_always_rain['resolution'] == 'days'

    # Test with it-stops-raining-in-days.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'it-stops-raining-in-days.yaml'), 'r') as file:
        rain_data = yaml.safe_load(file)
        # Extract forecast data from the YAML file
        forecast_data = rain_data['weather.openweathermap']['forecast']
        result_rain_data = json.loads(template.module.days_until_no_rain(forecast_data).strip())
        assert result_rain_data['time'] == '2025-06-12T11:00:00+00:00'
        assert result_rain_data['resolution'] == 'days' 