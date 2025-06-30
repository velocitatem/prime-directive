"""Decision Manager for handling decision data and persistence"""

import yaml
import os
from datetime import datetime
from typing import Dict, Any, List
import re


class DecisionManager:
    """Manages decision data and persistence"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def create_decision_slug(self, decision_text: str) -> str:
        """Create a slug from decision text (first 10 words, spaces replaced with -)"""
        words = decision_text.split()[:10]
        slug = "-".join(words)
        # Clean up the slug
        slug = re.sub(r'[^\w\-]', '', slug).lower()
        return slug
    
    def save_decision(self, decision_text: str, framework_results: List[Dict[str, Any]]) -> str:
        """Save decision and framework results to YAML file"""
        slug = self.create_decision_slug(decision_text)
        
        decision_data = {
            'decision': {
                'text': decision_text,
                'slug': slug,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'frameworks': framework_results,
            'metadata': {
                'total_frameworks': len(framework_results),
                'completed_frameworks': len([f for f in framework_results if f.get('result')])
            }
        }
        
        filename = f"{slug}.yaml"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            yaml.dump(decision_data, f, default_flow_style=False, indent=2)
        
        return filepath
    
    def load_decision(self, slug: str) -> Dict[str, Any]:
        """Load decision data from YAML file"""
        filename = f"{slug}.yaml"
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Decision file not found: {filename}")
        
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    def list_decisions(self) -> List[Dict[str, str]]:
        """List all saved decisions"""
        decisions = []
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.yaml'):
                try:
                    data = self.load_decision(filename[:-5])  # Remove .yaml extension
                    decisions.append({
                        'slug': data['decision']['slug'],
                        'text': data['decision']['text'][:100] + '...' if len(data['decision']['text']) > 100 else data['decision']['text'],
                        'created_at': data['decision']['created_at'],
                        'frameworks_count': data['metadata']['total_frameworks']
                    })
                except Exception:
                    continue
        
        return sorted(decisions, key=lambda x: x['created_at'], reverse=True)
    
    def update_decision(self, slug: str, framework_result: Dict[str, Any]) -> None:
        """Update decision with new framework result"""
        data = self.load_decision(slug)
        
        # Update or add framework result
        framework_name = framework_result['name']
        existing_index = None
        
        for i, framework in enumerate(data['frameworks']):
            if framework['name'] == framework_name:
                existing_index = i
                break
        
        if existing_index is not None:
            data['frameworks'][existing_index] = framework_result
        else:
            data['frameworks'].append(framework_result)
        
        # Update metadata
        data['decision']['last_updated'] = datetime.now().isoformat()
        data['metadata']['total_frameworks'] = len(data['frameworks'])
        data['metadata']['completed_frameworks'] = len([f for f in data['frameworks'] if f.get('result')])
        
        # Save updated data
        filename = f"{slug}.yaml"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=2)