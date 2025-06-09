import pytest
from jinja2 import Environment, FileSystemLoader

def test_hello_world_macro():
    """Test the hello_world macro."""
    # Setup Jinja2 environment with whitespace control
    env = Environment(
        loader=FileSystemLoader('usr/share/hassio/homeassistant'),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Get the template
    template = env.get_template('custom_templates/hello_world.jinja')
    
    # Test English version (default)
    result_en = template.module.hello_world().strip()
    assert result_en == "Hello World!"

    # Test German version
    result_de = template.module.hello_world('de').strip()
    assert result_de == "Hallo Welt!" 