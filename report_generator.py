import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from wcag_criteria import WCAG_CRITERIA, get_priority_for_result

class ReportGenerator:
    """
    Generates comprehensive accessibility reports combining automated and manual assessment results
    """
    
    def __init__(self):
        pass
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive accessibility report
        
        Args:
            analysis_results: Dictionary containing automated and manual assessment results
            
        Returns:
            Dictionary containing the complete accessibility report
        """
        report = {
            'meta': self._generate_meta_info(analysis_results),
            'summary': self._generate_summary(analysis_results),
            'automated_results': self._process_automated_results(analysis_results.get('automated_results')),
            'manual_assessment': self._process_manual_results(analysis_results.get('manual_results')),
            'wcag_compliance': self._generate_wcag_compliance_summary(analysis_results),
            'recommendations': self._generate_recommendations(analysis_results),
            'detailed_findings': self._generate_detailed_findings(analysis_results),
            'compliance_score': self._calculate_compliance_score(analysis_results)
        }
        
        return report
    
    def _generate_meta_info(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report metadata"""
        return {
            'url': results.get('url', 'Unknown'),
            'timestamp': results.get('timestamp', datetime.now().isoformat()),
            'wcag_version': '2.1',
            'levels_tested': results.get('wcag_levels', ['A', 'AA']),
            'testing_methods': {
                'automated': results.get('automated_results') is not None,
                'manual_ai': results.get('manual_results') is not None
            },
            'report_version': '1.0'
        }
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of findings"""
        automated_results = results.get('automated_results', {})
        manual_results = results.get('manual_results', {})
        
        # Count violations and issues
        automated_violations = len(automated_results.get('violations', []))
        manual_failures = sum(1 for r in manual_results.values() if r.get('status') == 'fail')
        manual_warnings = sum(1 for r in manual_results.values() if r.get('status') == 'warning')
        
        # Categorize by severity
        critical_issues = sum(1 for r in manual_results.values() 
                            if r.get('priority') == 'critical')
        high_issues = sum(1 for r in manual_results.values() 
                         if r.get('priority') == 'high') + \
                     sum(1 for v in automated_results.get('violations', []) 
                         if v.get('impact') == 'critical')
        
        return {
            'total_issues': automated_violations + manual_failures,
            'automated_violations': automated_violations,
            'manual_failures': manual_failures,
            'manual_warnings': manual_warnings,
            'critical_issues': critical_issues,
            'high_priority_issues': high_issues,
            'overall_status': self._determine_overall_status(results),
            'key_findings': self._extract_key_findings(results)
        }
    
    def _process_automated_results(self, automated_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and categorize automated test results"""
        if not automated_results:
            return {'available': False}
        
        violations = automated_results.get('violations', [])
        
        # Categorize by impact
        impact_summary = {'critical': 0, 'serious': 0, 'moderate': 0, 'minor': 0}
        wcag_violations = {}
        
        for violation in violations:
            impact = violation.get('impact', 'moderate')
            impact_summary[impact] = impact_summary.get(impact, 0) + 1
            
            # Group by WCAG tags
            for tag in violation.get('tags', []):
                if tag.startswith('wcag'):
                    wcag_violations[tag] = wcag_violations.get(tag, 0) + 1
        
        return {
            'available': True,
            'total_violations': len(violations),
            'impact_summary': impact_summary,
            'wcag_violations': wcag_violations,
            'violations': violations,
            'passes': len(automated_results.get('passes', [])),
            'incomplete': len(automated_results.get('incomplete', []))
        }
    
    def _process_manual_results(self, manual_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and categorize manual assessment results"""
        if not manual_results:
            return {'available': False}
        
        # Categorize by status and level
        status_summary = {'pass': 0, 'fail': 0, 'warning': 0, 'error': 0}
        level_summary = {'A': {'pass': 0, 'fail': 0, 'warning': 0},
                        'AA': {'pass': 0, 'fail': 0, 'warning': 0},
                        'AAA': {'pass': 0, 'fail': 0, 'warning': 0}}
        priority_summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for criteria_id, result in manual_results.items():
            status = result.get('status', 'error')
            level = result.get('level', 'A')
            priority = result.get('priority', 'medium')
            
            status_summary[status] = status_summary.get(status, 0) + 1
            if level in level_summary:
                level_summary[level][status] = level_summary[level].get(status, 0) + 1
            priority_summary[priority] = priority_summary.get(priority, 0) + 1
        
        return {
            'available': True,
            'total_criteria': len(manual_results),
            'status_summary': status_summary,
            'level_summary': level_summary,
            'priority_summary': priority_summary,
            'detailed_results': manual_results
        }
    
    def _generate_wcag_compliance_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate WCAG compliance summary by level"""
        manual_results = results.get('manual_results', {})
        automated_results = results.get('automated_results', {})
        
        compliance = {
            'A': {'total': 0, 'pass': 0, 'fail': 0, 'compliance_rate': 0},
            'AA': {'total': 0, 'pass': 0, 'fail': 0, 'compliance_rate': 0},
            'AAA': {'total': 0, 'pass': 0, 'fail': 0, 'compliance_rate': 0}
        }
        
        # Process manual results
        for criteria_id, result in manual_results.items():
            level = result.get('level', 'A')
            status = result.get('status', 'fail')
            
            if level in compliance:
                compliance[level]['total'] += 1
                if status == 'pass':
                    compliance[level]['pass'] += 1
                else:
                    compliance[level]['fail'] += 1
        
        # Calculate compliance rates
        for level in compliance:
            total = compliance[level]['total']
            if total > 0:
                compliance[level]['compliance_rate'] = round(
                    (compliance[level]['pass'] / total) * 100, 1
                )
        
        return compliance
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations for improvement"""
        recommendations = []
        
        # Process automated violations
        automated_results = results.get('automated_results', {})
        for violation in automated_results.get('violations', []):
            recommendations.append({
                'type': 'automated',
                'priority': self._map_impact_to_priority(violation.get('impact', 'moderate')),
                'title': violation.get('description', 'Unknown issue'),
                'description': violation.get('help', 'No description available'),
                'affected_elements': len(violation.get('nodes', [])),
                'wcag_reference': violation.get('tags', []),
                'help_url': violation.get('helpUrl', ''),
                'fix_suggestions': self._generate_fix_suggestions(violation)
            })
        
        # Process manual assessment results
        manual_results = results.get('manual_results', {})
        for criteria_id, result in manual_results.items():
            if result.get('status') in ['fail', 'warning']:
                recommendations.append({
                    'type': 'manual',
                    'priority': result.get('priority', 'medium'),
                    'title': f"{criteria_id}: {result.get('title', 'Unknown criteria')}",
                    'description': result.get('assessment', 'No assessment available'),
                    'wcag_level': result.get('level', 'A'),
                    'issues': result.get('issues', []),
                    'recommendations': result.get('recommendations', []),
                    'confidence': result.get('confidence', 0.5)
                })
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 2))
        
        return recommendations
    
    def _generate_detailed_findings(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed findings section"""
        return {
            'automated_findings': self._format_automated_findings(results.get('automated_results')),
            'manual_findings': self._format_manual_findings(results.get('manual_results')),
            'cross_references': self._generate_cross_references(results)
        }
    
    def _format_automated_findings(self, automated_results: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format automated findings for detailed reporting"""
        if not automated_results:
            return []
        
        findings = []
        for violation in automated_results.get('violations', []):
            finding = {
                'id': violation.get('id'),
                'description': violation.get('description'),
                'impact': violation.get('impact'),
                'help': violation.get('help'),
                'help_url': violation.get('helpUrl'),
                'wcag_tags': violation.get('tags', []),
                'affected_elements': []
            }
            
            for node in violation.get('nodes', []):
                element = {
                    'target': node.get('target', []),
                    'html': node.get('html', ''),
                    'failure_summary': node.get('failureSummary', ''),
                    'impact': node.get('impact')
                }
                finding['affected_elements'].append(element)
            
            findings.append(finding)
        
        return findings
    
    def _format_manual_findings(self, manual_results: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format manual assessment findings for detailed reporting"""
        if not manual_results:
            return []
        
        findings = []
        for criteria_id, result in manual_results.items():
            findings.append({
                'criteria_id': criteria_id,
                'title': result.get('title'),
                'level': result.get('level'),
                'status': result.get('status'),
                'priority': result.get('priority'),
                'confidence': result.get('confidence'),
                'assessment': result.get('assessment'),
                'issues': result.get('issues', []),
                'recommendations': result.get('recommendations', [])
            })
        
        return findings
    
    def _generate_cross_references(self, results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate cross-references between automated and manual findings"""
        cross_refs = {}
        
        # This could be enhanced to map automated violations to related manual criteria
        # For now, we'll provide a basic structure
        
        automated_results = results.get('automated_results', {})
        manual_results = results.get('manual_results', {})
        
        for violation in automated_results.get('violations', []):
            violation_id = violation.get('id', 'unknown')
            tags = violation.get('tags', [])
            
            related_manual = []
            for criteria_id in manual_results.keys():
                # Simple matching based on WCAG reference
                if any(criteria_id.replace('.', '') in tag for tag in tags):
                    related_manual.append(criteria_id)
            
            if related_manual:
                cross_refs[violation_id] = related_manual
        
        return cross_refs
    
    def _calculate_compliance_score(self, results: Dict[str, Any]) -> int:
        """Calculate overall compliance score (0-100)"""
        manual_results = results.get('manual_results', {})
        automated_results = results.get('automated_results', {})
        
        if not manual_results and not automated_results:
            return 0
        
        # Weight manual and automated results
        manual_weight = 0.7
        automated_weight = 0.3
        
        # Calculate manual score
        manual_score = 0
        if manual_results:
            total_manual = len(manual_results)
            passed_manual = sum(1 for r in manual_results.values() if r.get('status') == 'pass')
            manual_score = (passed_manual / total_manual) * 100 if total_manual > 0 else 0
        
        # Calculate automated score (inverse of violation rate)
        automated_score = 100  # Default to perfect if no automated results
        if automated_results:
            violations = len(automated_results.get('violations', []))
            passes = len(automated_results.get('passes', []))
            total_auto = violations + passes
            
            if total_auto > 0:
                automated_score = (passes / total_auto) * 100
        
        # Weighted average
        if manual_results and automated_results:
            overall_score = (manual_score * manual_weight) + (automated_score * automated_weight)
        elif manual_results:
            overall_score = manual_score
        else:
            overall_score = automated_score
        
        return round(overall_score)
    
    def _determine_overall_status(self, results: Dict[str, Any]) -> str:
        """Determine overall accessibility status"""
        compliance_score = self._calculate_compliance_score(results)
        
        if compliance_score >= 90:
            return 'Excellent'
        elif compliance_score >= 75:
            return 'Good'
        elif compliance_score >= 50:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def _extract_key_findings(self, results: Dict[str, Any]) -> List[str]:
        """Extract key findings for executive summary"""
        findings = []
        
        automated_results = results.get('automated_results', {})
        manual_results = results.get('manual_results', {})
        
        # Critical automated issues
        critical_violations = [v for v in automated_results.get('violations', []) 
                             if v.get('impact') == 'critical']
        if critical_violations:
            findings.append(f"{len(critical_violations)} critical accessibility violations found")
        
        # High priority manual issues
        high_priority_manual = [r for r in manual_results.values() 
                               if r.get('priority') == 'high']
        if high_priority_manual:
            findings.append(f"{len(high_priority_manual)} high-priority WCAG compliance issues")
        
        # Positive findings
        if not critical_violations and not high_priority_manual:
            findings.append("No critical accessibility issues detected")
        
        # Specific area concerns
        image_issues = sum(1 for r in manual_results.values() 
                          if '1.1.1' in r.get('criteria_id', '') and r.get('status') == 'fail')
        if image_issues:
            findings.append("Image accessibility needs attention")
        
        return findings[:5]  # Limit to top 5 findings
    
    def _map_impact_to_priority(self, impact: str) -> str:
        """Map axe-core impact levels to priority levels"""
        mapping = {
            'critical': 'critical',
            'serious': 'high',
            'moderate': 'medium',
            'minor': 'low'
        }
        return mapping.get(impact, 'medium')
    
    def _generate_fix_suggestions(self, violation: Dict[str, Any]) -> List[str]:
        """Generate specific fix suggestions for automated violations"""
        suggestions = []
        
        violation_id = violation.get('id', '')
        
        # Common fixes based on violation type
        if 'color-contrast' in violation_id:
            suggestions.extend([
                "Increase color contrast ratio to meet WCAG standards",
                "Use darker text on light backgrounds or lighter text on dark backgrounds",
                "Test with color contrast analyzers"
            ])
        elif 'image-alt' in violation_id:
            suggestions.extend([
                "Add descriptive alt text to images",
                "Use empty alt=\"\" for decorative images",
                "Ensure alt text conveys the same information as the image"
            ])
        elif 'heading' in violation_id:
            suggestions.extend([
                "Use proper heading hierarchy (h1, h2, h3, etc.)",
                "Don't skip heading levels",
                "Ensure headings describe the content that follows"
            ])
        elif 'label' in violation_id:
            suggestions.extend([
                "Associate labels with form controls",
                "Use aria-label or aria-labelledby when visible labels aren't possible",
                "Ensure all form inputs have accessible names"
            ])
        
        # Default suggestion if no specific ones found
        if not suggestions:
            suggestions.append(violation.get('help', 'Review the element and apply accessibility best practices'))
        
        return suggestions

    def export_report(self, report: Dict[str, Any], format_type: str = 'json') -> str:
        """
        Export report in specified format
        
        Args:
            report: The generated report dictionary
            format_type: Export format ('json', 'html', 'csv')
            
        Returns:
            Formatted report string
        """
        if format_type == 'json':
            return json.dumps(report, indent=2, ensure_ascii=False)
        elif format_type == 'html':
            return self._generate_html_report(report)
        elif format_type == 'csv':
            return self._generate_csv_report(report)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML version of the report"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Accessibility Report - {report['meta']['url']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .metric {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .violation {{ background: #fff5f5; border-left: 4px solid #dc3545; padding: 15px; margin: 10px 0; }}
                .pass {{ background: #f0fff4; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; }}
                .warning {{ background: #fffbf0; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
                .priority-critical {{ border-left-color: #dc3545; }}
                .priority-high {{ border-left-color: #fd7e14; }}
                .priority-medium {{ border-left-color: #ffc107; }}
                .priority-low {{ border-left-color: #28a745; }}
                h1, h2, h3 {{ color: #333; }}
                .score {{ font-size: 2em; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Web Accessibility Report</h1>
                <p><strong>URL:</strong> {report['meta']['url']}</p>
                <p><strong>Generated:</strong> {report['meta']['timestamp']}</p>
                <p><strong>WCAG Version:</strong> {report['meta']['wcag_version']}</p>
                <p><strong>Levels Tested:</strong> {', '.join(report['meta']['levels_tested'])}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>Compliance Score</h3>
                    <div class="score">{report['compliance_score']}%</div>
                </div>
                <div class="metric">
                    <h3>Overall Status</h3>
                    <div class="score">{report['summary']['overall_status']}</div>
                </div>
                <div class="metric">
                    <h3>Total Issues</h3>
                    <div class="score">{report['summary']['total_issues']}</div>
                </div>
                <div class="metric">
                    <h3>Critical Issues</h3>
                    <div class="score">{report['summary']['critical_issues']}</div>
                </div>
            </div>
            
            <h2>Key Findings</h2>
            <ul>
                {''.join(f'<li>{finding}</li>' for finding in report['summary']['key_findings'])}
            </ul>
            
            <h2>WCAG Compliance Summary</h2>
            <table>
                <tr>
                    <th>Level</th>
                    <th>Total Criteria</th>
                    <th>Passed</th>
                    <th>Failed</th>
                    <th>Compliance Rate</th>
                </tr>
                {self._generate_compliance_table_rows(report['wcag_compliance'])}
            </table>
            
            <h2>Recommendations</h2>
            {self._generate_recommendations_html(report['recommendations'])}
            
            <h2>Detailed Findings</h2>
            <pre>{json.dumps(report['detailed_findings'], indent=2)}</pre>
        </body>
        </html>
        """
        return html
    
    def _generate_compliance_table_rows(self, compliance: Dict[str, Any]) -> str:
        """Generate HTML table rows for compliance summary"""
        rows = []
        for level, data in compliance.items():
            rows.append(f"""
                <tr>
                    <td>WCAG {level}</td>
                    <td>{data['total']}</td>
                    <td>{data['pass']}</td>
                    <td>{data['fail']}</td>
                    <td>{data['compliance_rate']}%</td>
                </tr>
            """)
        return ''.join(rows)
    
    def _generate_recommendations_html(self, recommendations: List[Dict[str, Any]]) -> str:
        """Generate HTML for recommendations section"""
        html_parts = []
        
        for rec in recommendations[:10]:  # Show top 10 recommendations
            priority_class = f"priority-{rec['priority']}"
            html_parts.append(f"""
                <div class="violation {priority_class}">
                    <h4>{rec['title']}</h4>
                    <p><strong>Priority:</strong> {rec['priority'].title()}</p>
                    <p>{rec['description']}</p>
                    {'<p><strong>Recommendations:</strong></p><ul>' + ''.join(f'<li>{r}</li>' for r in rec.get('recommendations', [])) + '</ul>' if rec.get('recommendations') else ''}
                </div>
            """)
        
        return ''.join(html_parts)
    
    def _generate_csv_report(self, report: Dict[str, Any]) -> str:
        """Generate CSV version of key findings"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Type', 'Priority', 'Title', 'Description', 'WCAG Level', 'Status'])
        
        # Recommendations
        for rec in report['recommendations']:
            writer.writerow([
                rec.get('type', ''),
                rec.get('priority', ''),
                rec.get('title', ''),
                rec.get('description', '')[:200] + '...' if len(rec.get('description', '')) > 200 else rec.get('description', ''),
                rec.get('wcag_level', ''),
                'Issue' if rec.get('type') == 'manual' else 'Violation'
            ])
        
        return output.getvalue()
