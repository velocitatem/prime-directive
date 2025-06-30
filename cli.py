#!/usr/bin/env python3
"""Command Line Interface for Decision Making Toolkit"""

import argparse
import sys
import os
from typing import Dict, Any, List

# Add the tools directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frameworks import (
    SevenSFramework, VPCFramework, StrategicInflectionFramework,
    GameTheoryFramework, RiskRewardFramework
)
from cli.decision_manager import DecisionManager


class DecisionCLI:
    """Command Line Interface for Decision Making Frameworks"""
    
    def __init__(self):
        self.decision_manager = DecisionManager()
        self.frameworks = {
            '7s': SevenSFramework(),
            'vpc': VPCFramework(),
            'strategic': StrategicInflectionFramework(),
            'game': GameTheoryFramework(),
            'risk': RiskRewardFramework()
        }
    
    def list_frameworks(self):
        """List available frameworks"""
        print("\nAvailable Decision-Making Frameworks:")
        print("=====================================")
        for key, framework in self.frameworks.items():
            print(f"  {key}: {framework.name}")
        print()
    
    def list_decisions(self):
        """List saved decisions"""
        decisions = self.decision_manager.list_decisions()
        
        if not decisions:
            print("No saved decisions found.")
            return
        
        print("\nSaved Decisions:")
        print("===============")
        for decision in decisions:
            print(f"  {decision['slug']}")
            print(f"    Text: {decision['text']}")
            print(f"    Created: {decision['created_at']}")
            print(f"    Frameworks: {decision['frameworks_count']}")
            print()
    
    def create_decision(self, decision_text: str):
        """Create a new decision"""
        slug = self.decision_manager.create_decision_slug(decision_text)
        
        print(f"\nCreating decision: {slug}")
        print(f"Decision text: {decision_text}")
        
        # Save initial decision with empty frameworks
        filepath = self.decision_manager.save_decision(decision_text, [])
        print(f"Decision saved to: {filepath}")
        
        return slug
    
    def run_framework(self, decision_slug: str, framework_key: str):
        """Run a specific framework for a decision"""
        if framework_key not in self.frameworks:
            print(f"Framework '{framework_key}' not found. Use --list-frameworks to see available options.")
            return
        
        framework = self.frameworks[framework_key]
        
        print(f"\nRunning {framework.name} for decision: {decision_slug}")
        print("=" * 60)
        
        # Get required inputs
        required_inputs = framework.get_required_inputs()
        inputs = {}
        
        print("\nPlease provide the following inputs:")
        for field, description in required_inputs.items():
            if 'optional' in description.lower():
                value = input(f"{field} ({description}): ").strip()
                if value:
                    inputs[field] = value
            else:
                while True:
                    try:
                        value = input(f"{field} ({description}): ").strip()
                        if not value:
                            print("This field is required.")
                            continue
                        
                        # Try to convert to number if it looks like a score
                        if 'scale' in description.lower() or 'score' in description.lower():
                            inputs[field] = float(value)
                        else:
                            inputs[field] = value
                        break
                    except ValueError:
                        print("Please enter a valid number for score fields.")
        
        # Execute framework
        try:
            framework.set_inputs(inputs)
            result = framework.execute()
            
            # Display results
            self._display_results(result)
            
            # Save results
            framework_data = framework.to_dict()
            self.decision_manager.update_decision(decision_slug, framework_data)
            
            print(f"\nResults saved for decision: {decision_slug}")
            
        except Exception as e:
            print(f"Error running framework: {e}")
    
    def _display_results(self, result):
        """Display framework results"""
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        print(f"\nFramework: {result.framework_name}")
        
        if result.overall_score:
            print(f"Overall Score: {result.overall_score:.2f}")
        
        print("\nScores:")
        for key, score in result.scores.items():
            print(f"  {key.replace('_', ' ').title()}: {score}")
        
        print("\nRecommendations:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"  {i}. {rec}")
        
        if result.additional_data:
            print("\nAdditional Information:")
            for key, value in result.additional_data.items():
                if isinstance(value, list):
                    print(f"  {key.replace('_', ' ').title()}: {', '.join(map(str, value))}")
                else:
                    print(f"  {key.replace('_', ' ').title()}: {value}")
    
    def interactive_mode(self, decision_slug: str):
        """Interactive mode for applying multiple frameworks"""
        print(f"\nInteractive Decision Analysis Mode")
        print(f"Decision: {decision_slug}")
        print("=" * 60)
        
        while True:
            print("\nWhat would you like to do?")
            print("1. List available frameworks")
            print("2. Run a framework")
            print("3. View current results")
            print("4. Exit")
            
            choice = input("\nChoice (1-4): ").strip()
            
            if choice == '1':
                self.list_frameworks()
            elif choice == '2':
                framework_key = input("Enter framework key: ").strip().lower()
                self.run_framework(decision_slug, framework_key)
            elif choice == '3':
                self.view_decision_results(decision_slug)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter 1-4.")
    
    def view_decision_results(self, decision_slug: str):
        """View results for a decision"""
        try:
            data = self.decision_manager.load_decision(decision_slug)
            
            print(f"\nDecision: {data['decision']['text']}")
            print(f"Created: {data['decision']['created_at']}")
            print(f"Last Updated: {data['decision']['last_updated']}")
            print(f"Frameworks Applied: {data['metadata']['completed_frameworks']}")
            
            for framework_data in data['frameworks']:
                if framework_data.get('result'):
                    print(f"\n--- {framework_data['name']} ---")
                    result = framework_data['result']
                    if 'overall_score' in result and result['overall_score']:
                        print(f"Overall Score: {result['overall_score']:.2f}")
                    
                    print("Key Recommendations:")
                    for rec in result.get('recommendations', [])[:3]:
                        print(f"  • {rec}")
        
        except FileNotFoundError:
            print(f"Decision '{decision_slug}' not found.")


def main():
    parser = argparse.ArgumentParser(description='Decision Making Toolkit CLI')
    parser.add_argument('--list-frameworks', action='store_true', help='List available frameworks')
    parser.add_argument('--list-decisions', action='store_true', help='List saved decisions')
    parser.add_argument('--create', type=str, help='Create new decision with given text')
    parser.add_argument('--decision', type=str, help='Decision slug to work with')
    parser.add_argument('--framework', type=str, help='Framework to run (use with --decision)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode (use with --decision)')
    parser.add_argument('--view', action='store_true', help='View decision results (use with --decision)')
    
    args = parser.parse_args()
    cli = DecisionCLI()
    
    if args.list_frameworks:
        cli.list_frameworks()
    elif args.list_decisions:
        cli.list_decisions()
    elif args.create:
        slug = cli.create_decision(args.create)
        print(f"\nTo work with this decision, use: --decision {slug}")
    elif args.decision:
        if args.framework:
            cli.run_framework(args.decision, args.framework)
        elif args.interactive:
            cli.interactive_mode(args.decision)
        elif args.view:
            cli.view_decision_results(args.decision)
        else:
            print("Specify --framework, --interactive, or --view with --decision")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()