import pytest
from jinja2 import Environment, FileSystemLoader
import yaml
import os

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
    test_data_with_rain = {
        'weather': {
            'openweathermap': {
                'forecast': [
                    {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
                    {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 1.5},
                    {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
                ]
            }
        }
    }
    result_with_rain = template.module.has_rain(test_data_with_rain).strip()
    assert result_with_rain == "true"

    # Test without rain in forecast
    test_data_without_rain = {
        'weather': {
            'openweathermap': {
                'forecast': [
                    {'datetime': '2025-06-09T17:45:00+00:00', 'precipitation': 0},
                    {'datetime': '2025-06-09T17:46:00+00:00', 'precipitation': 0},
                    {'datetime': '2025-06-09T17:47:00+00:00', 'precipitation': 0}
                ]
            }
        }
    }
    result_without_rain = template.module.has_rain(test_data_without_rain).strip()
    assert result_without_rain == "false"

    # Test with no-rain-minutes.yaml data
    with open(os.path.join(os.path.dirname(__file__), 'no-rain-minutes.yaml'), 'r') as file:
        no_rain_data = yaml.safe_load(file)
        result_no_rain_data = template.module.has_rain(no_rain_data).strip()
        assert result_no_rain_data == "false" 