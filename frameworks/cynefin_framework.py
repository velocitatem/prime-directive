"""Cynefin Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class CynefinFramework(Framework):
    """Cynefin Sense-Making Framework"""

    def __init__(self):
        super().__init__("Cynefin Framework")

    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'clarity_level': 'Clarity of the problem definition (1-10 scale)',
            'cause_effect_visibility': 'Visibility of cause and effect relationships (1-10 scale)',
            'stakeholder_alignment': 'Stakeholder alignment on the issue (1-10 scale)',
            'time_pressure': 'Urgency or time pressure (1-10 scale)',
            'failure_impact': 'Potential impact of failure (1-10 scale)',
            'additional_notes': 'Additional context (optional)'
        }

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        required = ['clarity_level', 'cause_effect_visibility',
                    'stakeholder_alignment', 'time_pressure', 'failure_impact']
        for field in required:
            if field not in inputs:
                return False
            if not isinstance(inputs[field], (int, float)) or not (1 <= inputs[field] <= 10):
                return False
        return True

    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        clarity = float(inputs['clarity_level'])
        cause_effect = float(inputs['cause_effect_visibility'])
        alignment = float(inputs['stakeholder_alignment'])
        time_pressure = float(inputs['time_pressure'])
        impact = float(inputs['failure_impact'])

        complexity = (10 - clarity + 10 - cause_effect + 10 - alignment) / 3
        risk = (time_pressure + impact) / 2
        overall_score = (complexity + risk) / 2

        if complexity < 3 and risk < 3:
            domain = 'Obvious'
            approach = 'Sense – Categorize – Respond'
        elif complexity < 6:
            domain = 'Complicated'
            approach = 'Sense – Analyze – Respond'
        elif complexity < 8:
            domain = 'Complex'
            approach = 'Probe – Sense – Respond'
        else:
            domain = 'Chaotic'
            approach = 'Act – Sense – Respond'

        scores = {
            'complexity': complexity,
            'risk': risk,
            'domain': domain
        }

        recommendations = [
            f'Domain: {domain}',
            f'Recommended approach: {approach}'
        ]

        visualizations = {
            'position': {
                'complexity': complexity,
                'risk': risk,
                'domain': domain
            }
        }

        additional_data = {
            'approach': approach,
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
