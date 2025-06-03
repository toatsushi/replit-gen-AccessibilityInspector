from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.accessibility_checker import AccessibilityChecker
from src.ai_evaluator import AIEvaluator
from src.report_generator import ReportGenerator
from src.wcag_criteria import WCAG_CRITERIA
import json
from datetime import datetime
import base64
import traceback

AI_ASSESSMENT_FEATURE_FLAG = False  # AI-Powered Assessment機能のON/OFF切り替え

WCAG_LEVEL_TAGS = {
    "A": "wcag2a",
    "AA": "wcag2aa",
    "AAA": "wcag2aaa"
}

def main():
    st.set_page_config(
        page_title="WCAG Accessibility Evaluator",
        page_icon="♿",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("♿ WCAG Accessibility Evaluator")
    st.markdown("""
    This tool provides comprehensive web accessibility evaluation combining automated axe-core testing 
    with AI-powered manual assessment for complete WCAG compliance analysis.
    """)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # WCAG Version selection
        wcag_version = st.selectbox(
            "WCAG Version (※ 2.1のみサポート)",
            ["2.1", "2.2 (未サポート)", "2.0 (未サポート)"],
            index=0,
            help="現在サポートされているのはWCAG 2.1のみです。2.0, 2.2は未サポートです。"
        )
        
        # AI Provider selection
        if AI_ASSESSMENT_FEATURE_FLAG:
            ai_provider = st.selectbox(
                "AI Provider for Manual Assessment",
                ["OpenAI (GPT-4o)", "Anthropic (Claude)"],
                help="Choose the AI provider for evaluating manual assessment criteria"
            )
        else:
            ai_provider = None
        
        # WCAG Level selection
        wcag_levels = st.multiselect(
            "WCAG Compliance Levels",
            ["A", "AA", "AAA"],
            default=["A", "AA"],
            help="Select which WCAG levels to evaluate"
        )
        
        # Testing options
        st.subheader("Testing Options")
        include_automated = st.checkbox("Automated Testing (axe-core)", value=True)
        if AI_ASSESSMENT_FEATURE_FLAG:
            include_manual = st.checkbox("AI-Powered Manual Assessment", value=True)
        else:
            include_manual = False
        
        if not include_automated and not include_manual:
            st.error("Please select at least one testing method")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Website Analysis")
        url = st.text_input(
            "Enter URL to analyze",
            placeholder="https://example.com",
            help="Enter the full URL including http:// or https://"
        )
    
    with col2:
        st.subheader("Analysis")
        # 2.1以外が選択された場合はボタンを無効化
        wcag_version_supported = (wcag_version == "2.1")
        analyze_button = st.button(
            "🔍 Analyze Website",
            type="primary",
            use_container_width=True,
            disabled=not (include_automated or include_manual) or len(wcag_levels) == 0 or not wcag_version_supported
        )
        if not wcag_version_supported:
            st.warning("現在サポートされているのはWCAG 2.1のみです。2.0, 2.2は未サポートです。")
    
    if analyze_button and url:
        if not url.startswith(('http://', 'https://')):
            st.error("Please enter a valid URL starting with http:// or https://")
            return
        
        # Initialize progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize components
            status_text.text("Initializing accessibility checker...")
            progress_bar.progress(10)
            
            checker = AccessibilityChecker()
            if AI_ASSESSMENT_FEATURE_FLAG and ai_provider:
                ai_evaluator = AIEvaluator(provider=ai_provider.split()[0].lower())
            else:
                ai_evaluator = None
            report_generator = ReportGenerator()
            
            results = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'automated_results': None,
                'manual_results': None,
                'wcag_levels': wcag_levels,
                'wcag_version': wcag_version
            }
            
            # Automated testing with axe-core
            if include_automated:
                status_text.text("Running automated accessibility tests...")
                progress_bar.progress(30)
                
                automated_results = checker.run_axe_core_analysis(url, wcag_levels=wcag_levels)
                
                results['automated_results'] = automated_results
                
                st.success(f"Automated testing completed: {len(automated_results.get('violations', []))} violations found")
            
            # Manual assessment with AI
            if include_manual and AI_ASSESSMENT_FEATURE_FLAG and ai_evaluator:
                status_text.text("Running AI-powered manual assessment...")
                progress_bar.progress(60)
                page_content = checker.get_page_content(url)
                manual_results = ai_evaluator.evaluate_manual_criteria(page_content, wcag_levels, wcag_version)
                results['manual_results'] = manual_results
                st.success(f"AI-powered assessment completed for {len(manual_results)} criteria")
            else:
                results['manual_results'] = None
            
            status_text.text("Generating comprehensive report...")
            progress_bar.progress(90)
            
            # Generate report
            report = report_generator.generate_report(results)
            
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
            
            # Display results
            display_results(results, report)
            
        except Exception as e:
            print(e)
            traceback.print_exc()
            raise Exception(f"Error during axe-core analysis: {str(e)}")
            progress_bar.empty()
            status_text.empty()
    
    # Display example or help information
    if not url:
        st.markdown("---")
        st.subheader("How it works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🤖 Automated Testing**
            - Uses axe-core for comprehensive automated accessibility testing
            - Detects common WCAG violations
            - Provides specific element locations
            """)
        
        with col2:
            st.markdown("""
            **🧠 AI-Powered Assessment**
            - Evaluates criteria requiring human judgment
            - Uses advanced AI models (GPT-4o/Claude)
            - Provides contextual recommendations
            """)
        
        with col3:
            st.markdown("""
            **📊 Comprehensive Reports**
            - WCAG compliance overview
            - Detailed issue explanations
            - Actionable improvement suggestions
            """)

def display_results(results, report):
    """Display the analysis results in a comprehensive format"""
    
    st.markdown("---")
    st.header("📊 Accessibility Analysis Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_issues = len(results.get('automated_results', {}).get('violations', []))
        st.metric("Automated Issues", total_issues, delta=None)
    
    with col2:
        manual_results = results.get('manual_results') or {}
        manual_issues = sum(1 for criteria in manual_results.values() if criteria.get('status') == 'fail')
        st.metric("Manual Assessment Issues", manual_issues, delta=None)
    
    with col3:
        total_criteria = len(manual_results) if manual_results else 0
        st.metric("Total Criteria Evaluated", total_criteria, delta=None)
    
    with col4:
        compliance_score = report.get('compliance_score', 0)
        st.metric("Compliance Score", f"{compliance_score}%", 
                 delta=f"{compliance_score-50}%" if compliance_score != 0 else None)
    
    # Compliance overview chart
    if results.get('manual_results'):
        st.subheader("WCAG Compliance Overview")
        
        # Create compliance data for visualization
        compliance_data = []
        for criteria_id, criteria_data in results['manual_results'].items():
            compliance_data.append({
                'Criteria': criteria_id,
                'Level': criteria_data.get('level', 'Unknown'),
                'Status': criteria_data.get('status', 'unknown').title(),
                'Priority': criteria_data.get('priority', 'medium')
            })
        
        if compliance_data:
            df = pd.DataFrame(compliance_data)
            
            # Create status distribution chart
            status_counts = df['Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="WCAG Criteria Status Distribution",
                        color_discrete_map={'Pass': '#28a745', 'Fail': '#dc3545', 'Warning': '#ffc107'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results tabs
    tab1, tab2, tab3 = st.tabs(["🤖 Automated Results", "🧠 Manual Assessment", "📄 Full Report"])
    
    with tab1:
        display_automated_results(results.get('automated_results'))
    
    with tab2:
        display_manual_results(results.get('manual_results'))
    
    with tab3:
        display_full_report(report)
        
        # Export functionality
        st.subheader("Export Report")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download JSON Report"):
                json_str = json.dumps(report, indent=2, ensure_ascii=False)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="accessibility_report.json">Download JSON Report</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("📄 Download HTML Report"):
                html_report = generate_html_report(report)
                b64 = base64.b64encode(html_report.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="accessibility_report.html">Download HTML Report</a>'
                st.markdown(href, unsafe_allow_html=True)

def display_automated_results(automated_results):
    """Display automated testing results from axe-core"""
    if not automated_results:
        st.info("No automated testing results available")
        return
    
    violations = automated_results.get('violations', [])
    passes = automated_results.get('passes', [])
    
    st.subheader(f"Violations Found: {len(violations)}")
    
    if violations:
        for i, violation in enumerate(violations):
            with st.expander(f"🚫 {violation.get('description', 'Unknown issue')}", expanded=i < 3):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Impact:** {violation.get('impact', 'Unknown').title()}")
                    st.markdown(f"**Help:** {violation.get('help', 'No help available')}")
                    if violation.get('helpUrl'):
                        st.markdown(f"**Learn more:** [Documentation]({violation['helpUrl']})")
                
                with col2:
                    st.markdown(f"**WCAG Tags:** {', '.join(violation.get('tags', []))}")
                    st.markdown(f"**Elements affected:** {len(violation.get('nodes', []))}")
                
                # Show affected elements
                nodes = violation.get('nodes', [])
                if nodes:
                    st.markdown("**Affected Elements:**")
                    for node in nodes[:5]:  # Show first 5 elements
                        st.code(node.get('target', ['Unknown'])[0], language='css')
                        if node.get('html'):
                            st.code(node['html'][:200] + "..." if len(node['html']) > 200 else node['html'], 
                                   language='html')
    else:
        st.success("No automated violations found!")
    
    # Show passed tests summary
    if passes:
        st.subheader(f"Passed Tests: {len(passes)}")
        with st.expander("View passed accessibility tests"):
            for test in passes:
                st.write(f"✅ {test.get('description', 'Unknown test')}")

def display_manual_results(manual_results):
    """Display AI-powered manual assessment results"""
    if not manual_results:
        st.info("No manual assessment results available")
        return
    
    # Group by WCAG level
    levels = ['A', 'AA', 'AAA']
    
    for level in levels:
        level_criteria = {k: v for k, v in manual_results.items() if v.get('level') == level}
        
        if level_criteria:
            st.subheader(f"WCAG Level {level}")
            
            for criteria_id, criteria_data in level_criteria.items():
                status = criteria_data.get('status', 'unknown')
                status_icon = {"pass": "✅", "fail": "❌", "warning": "⚠️"}.get(status, "❓")
                
                with st.expander(f"{status_icon} {criteria_id}: {criteria_data.get('title', 'Unknown criteria')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Status:** {status.title()}")
                        st.markdown(f"**Assessment:** {criteria_data.get('assessment', 'No assessment available')}")
                        
                        if criteria_data.get('issues'):
                            st.markdown("**Issues identified:**")
                            for issue in criteria_data['issues']:
                                st.markdown(f"- {issue}")
                    
                    with col2:
                        st.markdown(f"**Priority:** {criteria_data.get('priority', 'medium').title()}")
                        st.markdown(f"**Level:** WCAG {level}")
                        
                        if criteria_data.get('recommendations'):
                            st.markdown("**Recommendations:**")
                            for rec in criteria_data['recommendations']:
                                st.markdown(f"- {rec}")

def display_full_report(report):
    """Display the complete accessibility report"""
    if not report:
        st.info("No report available")
        return
    
    st.json(report)

def generate_html_report(report):
    """Generate an HTML version of the accessibility report"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Accessibility Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
            .violation {{ background: #fff5f5; border-left: 4px solid #dc3545; padding: 15px; margin: 10px 0; }}
            .pass {{ background: #f0fff4; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; }}
            .warning {{ background: #fffbf0; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Web Accessibility Report</h1>
            <p><strong>URL:</strong> {report.get('meta', {}).get('url', 'Unknown')}</p>
            <p><strong>Generated:</strong> {report.get('meta', {}).get('timestamp', 'Unknown')}</p>
            <p><strong>WCAG Version:</strong> {report.get('meta', {}).get('wcag_version', '2.1')}</p>
            <p><strong>Compliance Score:</strong> {report.get('compliance_score', 0)}%</p>
        </div>
        
        <h2>Summary</h2>
        <p>This report provides a comprehensive analysis of web accessibility compliance.</p>
        
        <h2>Detailed Results</h2>
        <pre>{json.dumps(report, indent=2, ensure_ascii=False)}</pre>
    </body>
    </html>
    """
    return html_template

if __name__ == "__main__":
    main()
