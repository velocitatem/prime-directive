"""Risk-Reward Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class RiskRewardFramework(Framework):
    """Risk-Reward Matrix Framework for portfolio analysis"""
    
    def __init__(self):
        super().__init__("Risk-Reward Framework")
    
    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'risk_level': 'Risk assessment level (1-10 scale, 1=low risk, 10=high risk)',
            'reward_potential': 'Reward potential (1-10 scale, 1=low reward, 10=high reward)',
            'resource_requirements': 'Resource requirements (1-10 scale)',
            'success_probability': 'Success probability (0-100%)',
            'roi_projection': 'ROI projection percentage',
            'time_horizon': 'Time horizon in months',
            'option_description': 'Description of the strategic option',
            'additional_notes': 'Additional context (optional)'
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        required_fields = ['risk_level', 'reward_potential', 'resource_requirements', 
                          'success_probability', 'roi_projection', 'time_horizon', 'option_description']
        
        for field in required_fields:
            if field not in inputs:
                return False
        
        # Validate ranges
        if not (1 <= inputs['risk_level'] <= 10):
            return False
        if not (1 <= inputs['reward_potential'] <= 10):
            return False
        if not (1 <= inputs['resource_requirements'] <= 10):
            return False
        if not (0 <= inputs['success_probability'] <= 100):
            return False
        
        return True
    
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        risk = inputs['risk_level']
        reward = inputs['reward_potential']
        resources = inputs['resource_requirements']
        success_prob = inputs['success_probability'] / 100
        roi = inputs['roi_projection']
        time_horizon = inputs['time_horizon']
        
        # Calculate metrics
        risk_adjusted_return = reward * success_prob
        efficiency_ratio = risk_adjusted_return / resources if resources > 0 else 0
        expected_value = roi * success_prob
        
        # Quadrant classification
        if risk <= 5 and reward <= 5:
            quadrant = "Low Risk, Low Reward"
            priority = "Low"
        elif risk <= 5 and reward > 5:
            quadrant = "Low Risk, High Reward"
            priority = "High"
        elif risk > 5 and reward <= 5:
            quadrant = "High Risk, Low Reward"
            priority = "Very Low"
        else:
            quadrant = "High Risk, High Reward"
            priority = "Medium"
        
        # Overall score
        overall_score = (risk_adjusted_return + efficiency_ratio) / 2
        
        scores = {
            'risk_level': risk,
            'reward_potential': reward,
            'risk_adjusted_return': risk_adjusted_return,
            'efficiency_ratio': efficiency_ratio,
            'expected_value': expected_value,
            'resource_requirements': resources
        }
        
        recommendations = [
            f"Quadrant: {quadrant}",
            f"Priority: {priority}",
            f"Risk-adjusted return: {risk_adjusted_return:.2f}",
            f"Efficiency ratio: {efficiency_ratio:.2f}",
            f"Expected value: {expected_value:.1f}%"
        ]
        
        # Add specific recommendations based on quadrant
        if quadrant == "Low Risk, High Reward":
            recommendations.append("Recommended: Pursue this opportunity")
        elif quadrant == "High Risk, Low Reward":
            recommendations.append("Not recommended: High risk with low returns")
        elif quadrant == "High Risk, High Reward":
            recommendations.append("Consider with caution: High potential but high risk")
        else:
            recommendations.append("Low priority: Limited upside potential")
        
        visualizations = {
            'risk_reward_matrix': {
                'risk': risk,
                'reward': reward,
                'quadrant': quadrant
            },
            'metrics_chart': {
                'risk_adjusted_return': risk_adjusted_return,
                'efficiency_ratio': efficiency_ratio,
                'expected_value': expected_value
            }
        }
        
        additional_data = {
            'quadrant': quadrant,
            'priority': priority,
            'time_horizon': time_horizon,
            'success_probability': success_prob,
            'option_description': inputs['option_description'],
            'notes': inputs.get('additional_notes', '')
        }
        
        return FrameworkResult(
            framework_name=self.name,
            scores=scores,
            recommendations=recommendations,
            visualizations=visualizations,
            overall_score=overall_score,
            additional_data=additional_data
        )
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return self.result.visualizations if self.result else {}