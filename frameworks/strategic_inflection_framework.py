"""Strategic Inflection Points Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class StrategicInflectionFramework(Framework):
    """Andy Grove's Strategic Inflection Points Framework"""
    
    def __init__(self):
        super().__init__("Strategic Inflection Points Framework")
    
    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'market_signals': 'Market dynamics and early warning signs (1-10 scale)',
            'competitive_shifts': 'Changes in competitive landscape (1-10 scale)',
            'technology_impact': 'New technology adoption impact (1-10 scale)',
            'business_model_threat': 'Business model disruption threat (1-10 scale)',
            'internal_performance': 'Internal performance metrics (1-10 scale)',
            'frontline_feedback': 'Frontline employee insights (1-10 scale)',
            'signal_description': 'Description of key signals observed',
            'additional_notes': 'Additional context (optional)'
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        score_fields = ['market_signals', 'competitive_shifts', 'technology_impact', 
                       'business_model_threat', 'internal_performance', 'frontline_feedback']
        
        for field in score_fields:
            if field not in inputs:
                return False
            if not isinstance(inputs[field], (int, float)) or not (1 <= inputs[field] <= 10):
                return False
        
        return 'signal_description' in inputs
    
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        score_fields = ['market_signals', 'competitive_shifts', 'technology_impact', 
                       'business_model_threat', 'internal_performance', 'frontline_feedback']
        
        scores = {field: float(inputs[field]) for field in score_fields}
        
        # Calculate inflection risk
        threat_score = (scores['market_signals'] + scores['competitive_shifts'] + 
                       scores['technology_impact'] + scores['business_model_threat']) / 4
        
        readiness_score = (scores['internal_performance'] + scores['frontline_feedback']) / 2
        
        overall_risk = threat_score - readiness_score + 5  # Normalize to 1-10
        overall_risk = max(1, min(10, overall_risk))
        
        # Decision recommendation
        if overall_risk >= 7:
            decision = "Transform"
            risk_level = "High"
        elif overall_risk >= 5:
            decision = "Prepare"
            risk_level = "Medium"
        else:
            decision = "Defend"
            risk_level = "Low"
        
        recommendations = [
            f"Recommended action: {decision}",
            f"Inflection risk level: {risk_level}",
            f"Threat score: {threat_score:.1f}/10",
            f"Readiness score: {readiness_score:.1f}/10"
        ]
        
        if overall_risk >= 7:
            recommendations.append("Immediate strategic transformation required")
        elif overall_risk >= 5:
            recommendations.append("Prepare for potential transformation")
        else:
            recommendations.append("Continue current strategy with monitoring")
        
        visualizations = {
            'risk_matrix': {
                'threat_score': threat_score,
                'readiness_score': readiness_score,
                'overall_risk': overall_risk
            },
            'radar_chart': {
                'labels': [field.replace('_', ' ').title() for field in score_fields],
                'values': list(scores.values())
            }
        }
        
        additional_data = {
            'decision': decision,
            'risk_level': risk_level,
            'threat_score': threat_score,
            'readiness_score': readiness_score,
            'signal_description': inputs['signal_description'],
            'notes': inputs.get('additional_notes', '')
        }
        
        return FrameworkResult(
            framework_name=self.name,
            scores=scores,
            recommendations=recommendations,
            visualizations=visualizations,
            overall_score=overall_risk,
            additional_data=additional_data
        )
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return self.result.visualizations if self.result else {}