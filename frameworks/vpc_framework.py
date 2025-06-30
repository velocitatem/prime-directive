"""VPC (Value-Price-Cost) Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class VPCFramework(Framework):
    """Value-Price-Cost Framework for business model analysis"""
    
    def __init__(self):
        super().__init__("VPC Framework")
    
    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'cost': 'Total cost to create the offering (numeric)',
            'price': 'Market price point (numeric)',
            'value': 'Consumer perceived value (numeric)',
            'additional_notes': 'Any additional context (optional)'
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        required = ['cost', 'price', 'value']
        for field in required:
            if field not in inputs:
                return False
            if not isinstance(inputs[field], (int, float)) or inputs[field] <= 0:
                return False
        return True
    
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        cost = float(inputs['cost'])
        price = float(inputs['price'])
        value = float(inputs['value'])
        
        # Calculate key metrics
        margin = price - cost
        margin_percent = (margin / price) * 100 if price > 0 else 0
        value_premium = (value - price) / price * 100 if price > 0 else 0
        
        scores = {
            'cost': cost,
            'price': price,
            'value': value,
            'margin': margin,
            'margin_percent': margin_percent,
            'value_premium': value_premium
        }
        
        # Strategy classification
        if value > price and margin > 0:
            strategy = "Differentiation"
        elif price <= cost:
            strategy = "Loss Leader"
        elif margin_percent < 10:
            strategy = "Cost Leadership"
        else:
            strategy = "Balanced"
        
        recommendations = [
            f"Current strategy: {strategy}",
            f"Margin: ${margin:.2f} ({margin_percent:.1f}%)",
            f"Value premium: {value_premium:.1f}%"
        ]
        
        visualizations = {
            'triangle': {
                'cost': cost,
                'price': price,
                'value': value
            },
            'metrics': scores
        }
        
        return FrameworkResult(
            framework_name=self.name,
            scores=scores,
            recommendations=recommendations,
            visualizations=visualizations,
            additional_data={'strategy': strategy}
        )
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return self.result.visualizations if self.result else {}