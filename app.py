"""Flask Web Application for Decision Making Toolkit"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from frameworks import (
    SevenSFramework, VPCFramework, StrategicInflectionFramework,
    GameTheoryFramework, RiskRewardFramework, CynefinFramework
)
from cli.decision_manager import DecisionManager

app = Flask(__name__)
decision_manager = DecisionManager("data")

# Available frameworks
FRAMEWORKS = {
    '7s': SevenSFramework(),
    'vpc': VPCFramework(),
    'strategic': StrategicInflectionFramework(),
    'game': GameTheoryFramework(),
    'risk': RiskRewardFramework(),
    'cynefin': CynefinFramework()
}

@app.route('/')
def index():
    """Main dashboard"""
    decisions = decision_manager.list_decisions()
    return render_template('index.html', decisions=decisions, frameworks=FRAMEWORKS)

@app.route('/create_decision', methods=['GET', 'POST'])
def create_decision():
    """Create new decision"""
    if request.method == 'POST':
        decision_text = request.form['decision_text']
        slug = decision_manager.create_decision_slug(decision_text)
        decision_manager.save_decision(decision_text, [])
        return redirect(url_for('decision_detail', slug=slug))
    
    return render_template('create_decision.html')

@app.route('/decision/<slug>')
def decision_detail(slug):
    """Decision detail page"""
    try:
        data = decision_manager.load_decision(slug)
        return render_template('decision_detail.html', 
                             decision=data, 
                             frameworks=FRAMEWORKS,
                             slug=slug)
    except FileNotFoundError:
        return "Decision not found", 404

@app.route('/decision/<slug>/framework/<framework_key>')
def run_framework(slug, framework_key):
    """Run framework for decision"""
    if framework_key not in FRAMEWORKS:
        return "Framework not found", 404
    
    framework = FRAMEWORKS[framework_key]
    required_inputs = framework.get_required_inputs()
    
    return render_template('run_framework.html',
                         slug=slug,
                         framework_key=framework_key,
                         framework=framework,
                         required_inputs=required_inputs)

@app.route('/api/framework/<slug>/<framework_key>', methods=['POST'])
def api_run_framework(slug, framework_key):
    """API endpoint to run framework"""
    if framework_key not in FRAMEWORKS:
        return jsonify({'error': 'Framework not found'}), 404
    
    framework = FRAMEWORKS[framework_key]
    inputs = request.json
    
    try:
        # Convert string numbers to float for score fields
        for key, value in inputs.items():
            if isinstance(value, str) and value.strip():
                # Try to convert numeric fields
                if any(term in key.lower() for term in ['score', 'level', 'scale', 'probability', 'roi']):
                    try:
                        inputs[key] = float(value)
                    except ValueError:
                        pass
                # Convert numeric fields that end with numbers
                elif key in ['strategy', 'structure', 'systems', 'shared_values', 'style', 'staff', 'skills']:
                    try:
                        inputs[key] = float(value)
                    except ValueError:
                        pass
        
        # Remove empty string values
        inputs = {k: v for k, v in inputs.items() if v != ''}
        
        framework.set_inputs(inputs)
        result = framework.execute()
        
        # Save results
        framework_data = framework.to_dict()
        decision_manager.update_decision(slug, framework_data)
        
        return jsonify({
            'success': True,
            'result': result.__dict__
        })
    
    except Exception as e:
        print(f"Error in API: {e}")  # Debug print
        print(f"Inputs received: {inputs}")  # Debug print
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/decision/<slug>')
def api_decision_detail(slug):
    """API endpoint for decision data"""
    try:
        data = decision_manager.load_decision(slug)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Decision not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)