from typing import Dict, List, Optional, Union
import re
from pydantic import BaseModel

class MacroDefinition(BaseModel):
    """Model for storing macro definitions."""
    name: str
    template: str
    description: str
    parameters: List[str]
    metadata: Dict[str, Union[str, int, float]] = {}

class MacroManager:
    """Manages prompt macros and templates."""
    
    def __init__(self):
        """Initialize the macro manager."""
        self.macros: Dict[str, MacroDefinition] = {}
        self.macro_pattern = re.compile(r'\{\{([^}]+)\}\}')
    
    def register_macro(self, macro: MacroDefinition) -> None:
        """Register a new macro.
        
        Args:
            macro: The macro definition to register
        """
        self.macros[macro.name] = macro
    
    def unregister_macro(self, name: str) -> None:
        """Unregister a macro.
        
        Args:
            name: The name of the macro to unregister
        """
        if name in self.macros:
            del self.macros[name]
    
    def get_macro(self, name: str) -> Optional[MacroDefinition]:
        """Get a macro by name.
        
        Args:
            name: The name of the macro to get
            
        Returns:
            The macro definition if found, None otherwise
        """
        return self.macros.get(name)
    
    def list_macros(self) -> List[MacroDefinition]:
        """List all registered macros.
        
        Returns:
            List of all registered macro definitions
        """
        return list(self.macros.values())
    
    def expand_macro(self, name: str, parameters: Dict[str, str]) -> Optional[str]:
        """Expand a macro with the given parameters.
        
        Args:
            name: The name of the macro to expand
            parameters: Dictionary of parameter values
            
        Returns:
            The expanded macro text if successful, None otherwise
        """
        macro = self.get_macro(name)
        if not macro:
            return None
        
        try:
            # Check if all required parameters are provided
            missing_params = set(macro.parameters) - set(parameters.keys())
            if missing_params:
                raise ValueError(f"Missing required parameters: {missing_params}")
            
            # Expand the template
            expanded = macro.template
            for param_name, param_value in parameters.items():
                expanded = expanded.replace(f"{{{{{param_name}}}}}", param_value)
            
            return expanded
            
        except Exception as e:
            print(f"Error expanding macro {name}: {str(e)}")
            return None
    
    def find_macros_in_text(self, text: str) -> List[str]:
        """Find all macro references in a text.
        
        Args:
            text: The text to search for macro references
            
        Returns:
            List of macro names found in the text
        """
        matches = self.macro_pattern.findall(text)
        return [match.strip() for match in matches]
    
    def expand_text(self, text: str, parameters: Dict[str, Dict[str, str]]) -> str:
        """Expand all macros in a text.
        
        Args:
            text: The text containing macro references
            parameters: Dictionary mapping macro names to their parameter values
            
        Returns:
            The text with all macros expanded
        """
        expanded = text
        for macro_name in self.find_macros_in_text(text):
            if macro_name in parameters:
                expanded_macro = self.expand_macro(macro_name, parameters[macro_name])
                if expanded_macro:
                    expanded = expanded.replace(f"{{{{{macro_name}}}}}", expanded_macro)
        return expanded 