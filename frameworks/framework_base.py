"""Base Framework class for decision-making tools"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json


@dataclass
class FrameworkResult:
    """Standard result structure for all frameworks"""
    framework_name: str
    scores: Dict[str, float]
    recommendations: List[str]
    visualizations: Dict[str, Any]
    overall_score: Optional[float] = None
    additional_data: Dict[str, Any] = None


class Framework(ABC):
    """Abstract base class for decision-making frameworks"""
    
    def __init__(self, name: str):
        self.name = name
        self.inputs = {}
        self.result = None
    
    @abstractmethod
    def get_required_inputs(self) -> Dict[str, str]:
        """Return dictionary of required input fields and their descriptions"""
        pass
    
    @abstractmethod
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate that inputs are complete and valid"""
        pass
    
    @abstractmethod
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        """Execute framework calculation and return results"""
        pass
    
    @abstractmethod
    def get_visualization_data(self) -> Dict[str, Any]:
        """Return data formatted for visualization"""
        pass
    
    def set_inputs(self, inputs: Dict[str, Any]) -> None:
        """Set inputs for the framework"""
        if self.validate_inputs(inputs):
            self.inputs = inputs
        else:
            raise ValueError("Invalid inputs provided")
    
    def execute(self) -> FrameworkResult:
        """Execute the framework with current inputs"""
        if not self.inputs:
            raise ValueError("No inputs provided")
        
        self.result = self.calculate(self.inputs)
        return self.result
    
    def get_input_prompts(self) -> List[str]:
        """Get user-friendly prompts for collecting inputs"""
        required = self.get_required_inputs()
        return [f"{field}: {description}" for field, description in required.items()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert framework state to dictionary"""
        return {
            'name': self.name,
            'inputs': self.inputs,
            'result': self.result.__dict__ if self.result else None
        }
    
    def export_data(self) -> str:
        """Export framework data as JSON"""
        return json.dumps(self.to_dict(), indent=2, default=str)