"""McKinsey 7S Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class SevenSFramework(Framework):
    """McKinsey 7S Framework for organizational alignment analysis"""
    
    def __init__(self):
        super().__init__("McKinsey 7S Framework")
        self.s_elements = [
            'strategy', 'structure', 'systems', 'shared_values', 
            'style', 'staff', 'skills'
        ]
    
    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'strategy': 'Current strategic approach and focus (1-10 scale)',
            'structure': 'Organizational hierarchy and reporting effectiveness (1-10 scale)',
            'systems': 'Processes, procedures, and IT infrastructure quality (1-10 scale)',
            'shared_values': 'Company culture and core beliefs alignment (1-10 scale)',
            'style': 'Leadership approach and management effectiveness (1-10 scale)',
            'staff': 'Human resources and organizational capabilities (1-10 scale)',
            'skills': 'Core competencies and capabilities strength (1-10 scale)',
            'additional_notes': 'Any additional context or observations (optional)'
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate 7S inputs"""
        for element in self.s_elements:
            if element not in inputs:
                return False
            
            score = inputs[element]
            if not isinstance(score, (int, float)) or not (1 <= score <= 10):
                return False
        
        return True
    
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        """Calculate 7S Framework results"""
        scores = {element: float(inputs[element]) for element in self.s_elements}
        
        # Calculate overall alignment score
        overall_score = sum(scores.values()) / len(scores)
        
        # Generate recommendations based on scores
        recommendations = self._generate_recommendations(scores, overall_score)
        
        # Prepare visualization data
        visualizations = {
            'radar_chart': {
                'labels': [s.replace('_', ' ').title() for s in self.s_elements],
                'values': list(scores.values()),
                'max_value': 10
            },
            'bar_chart': {
                'categories': list(scores.keys()),
                'values': list(scores.values())
            },
            'alignment_gauge': {
                'score': overall_score,
                'max_score': 10,
                'threshold': 7.5
            }
        }
        
        additional_data = {
            'weak_areas': [k for k, v in scores.items() if v < 6],
            'strong_areas': [k for k, v in scores.items() if v >= 8],
            'alignment_status': 'Strong' if overall_score >= 7.5 else 'Weak',
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
    
    def _generate_recommendations(self, scores: Dict[str, float], overall_score: float) -> List[str]:
        """Generate recommendations based on 7S scores"""
        recommendations = []
        
        if overall_score >= 7.5:
            recommendations.append("Strong organizational alignment detected - good foundation for strategic initiatives")
        else:
            recommendations.append("Organizational alignment needs improvement before major strategic moves")
        
        # Identify weak areas
        weak_areas = [k for k, v in scores.items() if v < 6]
        if weak_areas:
            recommendations.append(f"Priority improvement areas: {', '.join(weak_areas)}")
        
        # Specific recommendations for each S
        if scores['strategy'] < 6:
            recommendations.append("Strategy: Clarify strategic direction and communicate vision more effectively")
        
        if scores['structure'] < 6:
            recommendations.append("Structure: Review organizational hierarchy and reporting relationships")
        
        if scores['systems'] < 6:
            recommendations.append("Systems: Upgrade processes and technology infrastructure")
        
        if scores['shared_values'] < 6:
            recommendations.append("Shared Values: Strengthen company culture and value alignment")
        
        if scores['style'] < 6:
            recommendations.append("Style: Develop leadership capabilities and management approach")
        
        if scores['staff'] < 6:
            recommendations.append("Staff: Invest in talent development and organizational capabilities")
        
        if scores['skills'] < 6:
            recommendations.append("Skills: Build core competencies and technical capabilities")
        
        return recommendations
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Return visualization data for the 7S framework"""
        if not self.result:
            return {}
        
        return self.result.visualizations