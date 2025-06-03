import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
import anthropic
from wcag_criteria import WCAG_CRITERIA

class AIEvaluator:
    """
    Handles AI-powered evaluation of manual accessibility criteria
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self.openai_client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.provider == "anthropic":
            self.anthropic_client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError("Provider must be either 'openai' or 'anthropic'")
    
    def evaluate_manual_criteria(self, page_content: Dict[str, Any], wcag_levels: List[str]) -> Dict[str, Any]:
        """
        Evaluate manual accessibility criteria using AI
        
        Args:
            page_content: Dictionary containing page content and structure
            wcag_levels: List of WCAG levels to evaluate (A, AA, AAA)
            
        Returns:
            Dictionary containing evaluation results for each criteria
        """
        results = {}
        
        # Filter criteria by requested WCAG levels
        criteria_to_evaluate = {
            criteria_id: criteria_data 
            for criteria_id, criteria_data in WCAG_CRITERIA.items()
            if criteria_data['level'] in wcag_levels and criteria_data['requires_manual_assessment']
        }
        
        for criteria_id, criteria_data in criteria_to_evaluate.items():
            try:
                evaluation = self._evaluate_single_criteria(criteria_id, criteria_data, page_content)
                results[criteria_id] = evaluation
            except Exception as e:
                results[criteria_id] = {
                    'status': 'error',
                    'error': str(e),
                    'level': criteria_data['level'],
                    'title': criteria_data['title']
                }
        
        return results
    
    def _evaluate_single_criteria(self, criteria_id: str, criteria_data: Dict[str, Any], page_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single WCAG criteria using AI
        
        Args:
            criteria_id: WCAG criteria identifier (e.g., "1.1.1")
            criteria_data: Criteria information from WCAG_CRITERIA
            page_content: Page content to analyze
            
        Returns:
            Dictionary containing evaluation result
        """
        # Prepare context for AI evaluation
        evaluation_prompt = self._create_evaluation_prompt(criteria_id, criteria_data, page_content)
        
        if self.provider == "openai":
            response = self._evaluate_with_openai(evaluation_prompt)
        else:
            response = self._evaluate_with_anthropic(evaluation_prompt)
        
        # Parse and structure the response
        return self._parse_ai_response(response, criteria_data)
    
    def _create_evaluation_prompt(self, criteria_id: str, criteria_data: Dict[str, Any], page_content: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for AI evaluation"""
        
        prompt = f"""
You are an expert web accessibility auditor specializing in WCAG compliance evaluation.

**WCAG Criteria to Evaluate:**
- ID: {criteria_id}
- Title: {criteria_data['title']}
- Level: {criteria_data['level']}
- Description: {criteria_data['description']}

**Evaluation Guidelines:**
{criteria_data['evaluation_guidelines']}

**Page Content Analysis:**

**URL:** {page_content.get('url', 'Unknown')}
**Page Title:** {page_content.get('title', 'No title')}

**Headings Structure:**
{json.dumps(page_content.get('headings', [])[:10], indent=2)}

**Images (first 10):**
{json.dumps(page_content.get('images', [])[:10], indent=2)}

**Links (first 10):**
{json.dumps(page_content.get('links', [])[:10], indent=2)}

**Forms:**
{json.dumps(page_content.get('forms', []), indent=2)}

**Meta Tags:**
{json.dumps(page_content.get('meta_tags', {}), indent=2)}

**Text Content (excerpt):**
{page_content.get('text_content', '')[:1000]}

**HTML Structure (excerpt):**
{page_content.get('html_structure', '')[:2000]}

**Required Response Format:**
Provide your evaluation in JSON format with the following structure:
{{
    "status": "pass|fail|warning",
    "confidence": 0.0-1.0,
    "assessment": "Detailed explanation of your evaluation",
    "issues": ["List of specific issues found (if any)"],
    "recommendations": ["Specific actionable recommendations"],
    "priority": "low|medium|high|critical"
}}

**Evaluation Instructions:**
1. Thoroughly analyze the provided page content against the WCAG criteria
2. Consider both the presence and quality of accessibility features
3. Provide specific, actionable recommendations
4. Assign appropriate priority based on impact and user experience
5. Be conservative - if uncertain, lean towards "warning" status with recommendations

Please evaluate this page against WCAG criteria {criteria_id} and provide your assessment in the required JSON format.
"""
        
        return prompt
    
    def _evaluate_with_openai(self, prompt: str) -> str:
        """Evaluate using OpenAI GPT-4o"""
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert web accessibility auditor. Analyze the provided content and respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI evaluation failed: {str(e)}")
    
    def _evaluate_with_anthropic(self, prompt: str) -> str:
        """Evaluate using Anthropic Claude"""
        try:
            # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt + "\n\nPlease respond with valid JSON only, no additional text or explanation outside the JSON structure."
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic evaluation failed: {str(e)}")
    
    def _parse_ai_response(self, response: str, criteria_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Try to parse JSON response
            evaluation = json.loads(response)
            
            # Validate required fields
            required_fields = ['status', 'confidence', 'assessment', 'issues', 'recommendations', 'priority']
            for field in required_fields:
                if field not in evaluation:
                    evaluation[field] = self._get_default_value(field)
            
            # Add metadata
            evaluation['level'] = criteria_data['level']
            evaluation['title'] = criteria_data['title']
            evaluation['criteria_id'] = criteria_data.get('id', 'unknown')
            
            # Validate and clean values
            evaluation['status'] = evaluation['status'].lower()
            if evaluation['status'] not in ['pass', 'fail', 'warning']:
                evaluation['status'] = 'warning'
            
            evaluation['priority'] = evaluation['priority'].lower()
            if evaluation['priority'] not in ['low', 'medium', 'high', 'critical']:
                evaluation['priority'] = 'medium'
            
            evaluation['confidence'] = max(0.0, min(1.0, float(evaluation['confidence'])))
            
            # Ensure lists
            if not isinstance(evaluation['issues'], list):
                evaluation['issues'] = [str(evaluation['issues'])]
            
            if not isinstance(evaluation['recommendations'], list):
                evaluation['recommendations'] = [str(evaluation['recommendations'])]
            
            return evaluation
            
        except json.JSONDecodeError:
            # Fallback for invalid JSON
            return {
                'status': 'error',
                'confidence': 0.0,
                'assessment': f'Failed to parse AI response: {response[:200]}...',
                'issues': ['AI response parsing failed'],
                'recommendations': ['Manual review required'],
                'priority': 'medium',
                'level': criteria_data['level'],
                'title': criteria_data['title'],
                'criteria_id': criteria_data.get('id', 'unknown')
            }
    
    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing fields"""
        defaults = {
            'status': 'warning',
            'confidence': 0.5,
            'assessment': 'Assessment not available',
            'issues': [],
            'recommendations': [],
            'priority': 'medium'
        }
        return defaults.get(field, None)
    
    def evaluate_batch_criteria(self, page_content: Dict[str, Any], criteria_list: List[str]) -> Dict[str, Any]:
        """
        Evaluate multiple criteria in a single AI call for efficiency
        
        Args:
            page_content: Page content to analyze
            criteria_list: List of criteria IDs to evaluate
            
        Returns:
            Dictionary with evaluation results for each criteria
        """
        # This could be implemented for more efficient batch processing
        # For now, we'll use individual evaluations
        results = {}
        
        for criteria_id in criteria_list:
            if criteria_id in WCAG_CRITERIA:
                criteria_data = WCAG_CRITERIA[criteria_id]
                results[criteria_id] = self._evaluate_single_criteria(criteria_id, criteria_data, page_content)
        
        return results
