"""Game Theory Framework Implementation"""

from typing import Dict, Any, List
from .framework_base import Framework, FrameworkResult


class GameTheoryFramework(Framework):
    """Game Theory Framework for competitive decision analysis"""
    
    def __init__(self):
        super().__init__("Game Theory Framework")
    
    def get_required_inputs(self) -> Dict[str, str]:
        return {
            'our_action_1': 'Our first possible action',
            'our_action_2': 'Our second possible action',
            'competitor_action_1': 'Competitor first possible action',
            'competitor_action_2': 'Competitor second possible action',
            'payoff_11': 'Our payoff when both choose action 1 (numeric)',
            'payoff_12': 'Our payoff when we choose 1, competitor chooses 2 (numeric)',
            'payoff_21': 'Our payoff when we choose 2, competitor chooses 1 (numeric)',
            'payoff_22': 'Our payoff when both choose action 2 (numeric)',
            'competitor_payoff_11': 'Competitor payoff when both choose action 1 (numeric)',
            'competitor_payoff_12': 'Competitor payoff when we choose 1, they choose 2 (numeric)',
            'competitor_payoff_21': 'Competitor payoff when we choose 2, they choose 1 (numeric)',
            'competitor_payoff_22': 'Competitor payoff when both choose action 2 (numeric)',
            'additional_notes': 'Additional context (optional)'
        }
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        required_text = ['our_action_1', 'our_action_2', 'competitor_action_1', 'competitor_action_2']
        required_numeric = ['payoff_11', 'payoff_12', 'payoff_21', 'payoff_22',
                           'competitor_payoff_11', 'competitor_payoff_12', 
                           'competitor_payoff_21', 'competitor_payoff_22']
        
        for field in required_text + required_numeric:
            if field not in inputs:
                return False
        
        for field in required_numeric:
            if not isinstance(inputs[field], (int, float)):
                return False
        
        return True
    
    def calculate(self, inputs: Dict[str, Any]) -> FrameworkResult:
        # Build payoff matrix
        our_payoffs = [
            [inputs['payoff_11'], inputs['payoff_12']],
            [inputs['payoff_21'], inputs['payoff_22']]
        ]
        
        competitor_payoffs = [
            [inputs['competitor_payoff_11'], inputs['competitor_payoff_12']],
            [inputs['competitor_payoff_21'], inputs['competitor_payoff_22']]
        ]
        
        # Find Nash equilibrium
        nash_equilibria = []
        
        for i in range(2):
            for j in range(2):
                # Check if (i,j) is Nash equilibrium
                our_best_response = True
                competitor_best_response = True
                
                # Check if we have incentive to deviate
                for alt_i in range(2):
                    if alt_i != i and our_payoffs[alt_i][j] > our_payoffs[i][j]:
                        our_best_response = False
                        break
                
                # Check if competitor has incentive to deviate
                for alt_j in range(2):
                    if alt_j != j and competitor_payoffs[i][alt_j] > competitor_payoffs[i][j]:
                        competitor_best_response = False
                        break
                
                if our_best_response and competitor_best_response:
                    nash_equilibria.append((i, j))
        
        # Generate recommendations
        recommendations = []
        
        if nash_equilibria:
            for i, j in nash_equilibria:
                our_action = inputs[f'our_action_{i+1}']
                competitor_action = inputs[f'competitor_action_{j+1}']
                our_payoff = our_payoffs[i][j]
                recommendations.append(f"Nash equilibrium: {our_action} vs {competitor_action} (payoff: {our_payoff})")
        else:
            recommendations.append("No pure strategy Nash equilibrium found")
        
        # Find dominant strategies
        dominant_strategy = self._find_dominant_strategy(our_payoffs)
        if dominant_strategy is not None:
            action_name = inputs[f'our_action_{dominant_strategy+1}']
            recommendations.append(f"Dominant strategy: {action_name}")
        
        scores = {
            'payoff_scenario_11': our_payoffs[0][0],
            'payoff_scenario_12': our_payoffs[0][1],
            'payoff_scenario_21': our_payoffs[1][0],
            'payoff_scenario_22': our_payoffs[1][1]
        }
        
        visualizations = {
            'payoff_matrix': {
                'our_actions': [inputs['our_action_1'], inputs['our_action_2']],
                'competitor_actions': [inputs['competitor_action_1'], inputs['competitor_action_2']],
                'our_payoffs': our_payoffs,
                'competitor_payoffs': competitor_payoffs
            },
            'nash_equilibria': nash_equilibria
        }
        
        additional_data = {
            'nash_equilibria': nash_equilibria,
            'dominant_strategy': dominant_strategy,
            'notes': inputs.get('additional_notes', '')
        }
        
        return FrameworkResult(
            framework_name=self.name,
            scores=scores,
            recommendations=recommendations,
            visualizations=visualizations,
            additional_data=additional_data
        )
    
    def _find_dominant_strategy(self, payoff_matrix: List[List[float]]) -> int:
        """Find if there's a dominant strategy"""
        for i in range(2):
            dominates = True
            for alt_i in range(2):
                if alt_i != i:
                    for j in range(2):
                        if payoff_matrix[i][j] <= payoff_matrix[alt_i][j]:
                            dominates = False
                            break
                    if not dominates:
                        break
            if dominates:
                return i
        return None
    
    def get_visualization_data(self) -> Dict[str, Any]:
        return self.result.visualizations if self.result else {}