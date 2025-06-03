"""
WCAG 2.1 Success Criteria definitions with evaluation guidelines
Focus on criteria that require manual assessment and human judgment
"""

WCAG_CRITERIA = {
    "1.1.1": {
        "id": "1.1.1",
        "title": "Non-text Content",
        "level": "A",
        "description": "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Evaluate whether:
        1. Images have meaningful alt text that conveys the same information
        2. Decorative images have empty alt attributes (alt="")
        3. Complex images (charts, graphs) have adequate descriptions
        4. Alt text is concise and describes the content/function, not appearance
        5. Images of text have alt text that includes the text content
        6. CAPTCHAs have alternative methods available
        """
    },
    
    "1.2.1": {
        "id": "1.2.1", 
        "title": "Audio-only and Video-only (Prerecorded)",
        "level": "A",
        "description": "For prerecorded audio-only and prerecorded video-only media, alternatives are provided.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Check for:
        1. Audio-only content has text transcripts
        2. Video-only content has audio descriptions or text alternatives
        3. Alternatives provide equivalent information
        4. Transcripts are accurate and complete
        5. Alternative formats are easily accessible
        """
    },
    
    "1.2.2": {
        "id": "1.2.2",
        "title": "Captions (Prerecorded)",
        "level": "A", 
        "description": "Captions are provided for all prerecorded audio content in synchronized media.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Verify that:
        1. All videos with audio have captions
        2. Captions are accurate and synchronized
        3. Captions include relevant sound effects and speaker identification
        4. Caption controls are accessible
        5. Captions don't obscure important visual content
        """
    },
    
    "1.3.1": {
        "id": "1.3.1",
        "title": "Info and Relationships", 
        "level": "A",
        "description": "Information, structure, and relationships conveyed through presentation can be programmatically determined.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Assess whether:
        1. Heading structure reflects content hierarchy
        2. Lists are properly marked up with ul, ol, li elements
        3. Tables use proper headers and structure
        4. Form labels are properly associated with inputs
        5. Visual relationships are also programmatically determinable
        6. Semantic markup is used appropriately
        """
    },
    
    "1.3.2": {
        "id": "1.3.2",
        "title": "Meaningful Sequence",
        "level": "A",
        "description": "When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Check that:
        1. Content order makes sense when read linearly
        2. CSS positioning doesn't break logical flow
        3. Tab order follows visual layout
        4. Reading order matches visual presentation
        5. Multi-column layouts maintain proper sequence
        """
    },
    
    "1.3.3": {
        "id": "1.3.3",
        "title": "Sensory Characteristics",
        "level": "A", 
        "description": "Instructions provided for understanding and operating content do not rely solely on sensory characteristics.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Ensure instructions don't rely solely on:
        1. Shape (click the round button)
        2. Size (use the large text box)
        3. Visual location (button on the right)
        4. Orientation (portrait/landscape)
        5. Sound (beep indicates error)
        Instructions should include multiple identifiers
        """
    },
    
    "1.4.1": {
        "id": "1.4.1",
        "title": "Use of Color",
        "level": "A",
        "description": "Color is not used as the only visual means of conveying information.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Verify that information isn't conveyed by color alone:
        1. Required form fields have additional indicators
        2. Charts/graphs use patterns or labels
        3. Links are distinguishable without color
        4. Error messages don't rely only on red color
        5. Status information has non-color indicators
        """
    },
    
    "1.4.3": {
        "id": "1.4.3",
        "title": "Contrast (Minimum)",
        "level": "AA",
        "description": "Text has a contrast ratio of at least 4.5:1 (3:1 for large text).",
        "requires_manual_assessment": False,  # Can be automated
        "evaluation_guidelines": """
        This can be automatically tested, but manual verification may be needed for:
        1. Text over images or gradients
        2. Dynamic content that changes color
        3. Brand colors that may not meet requirements
        4. Interactive states (hover, focus, active)
        """
    },
    
    "2.1.1": {
        "id": "2.1.1",
        "title": "Keyboard",
        "level": "A",
        "description": "All functionality is available from a keyboard.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Test that all interactive elements can be:
        1. Reached using only keyboard navigation
        2. Activated using keyboard (Enter, Space)
        3. Used without requiring specific timings
        4. Custom controls have keyboard support
        5. No keyboard traps exist
        """
    },
    
    "2.1.2": {
        "id": "2.1.2", 
        "title": "No Keyboard Trap",
        "level": "A",
        "description": "If keyboard focus can be moved to a component, it can be moved away using only keyboard.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Ensure users can navigate away from all components:
        1. No elements trap keyboard focus
        2. Modal dialogs can be closed with keyboard
        3. Custom widgets allow focus to move out
        4. If focus is restricted, standard exit methods work
        5. Instructions are provided for non-standard navigation
        """
    },
    
    "2.2.1": {
        "id": "2.2.1",
        "title": "Timing Adjustable", 
        "level": "A",
        "description": "Users can turn off, adjust, or extend time limits.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        For content with time limits, verify:
        1. Users can turn off the time limit, OR
        2. Users can adjust the time limit (at least 10x default), OR  
        3. Users are warned and can extend with simple action
        4. Real-time events are essential exceptions
        5. Time limits over 20 hours are exempt
        """
    },
    
    "2.2.2": {
        "id": "2.2.2",
        "title": "Pause, Stop, Hide",
        "level": "A",
        "description": "Users can pause, stop, or hide moving, blinking, or auto-updating information.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        For auto-playing content, check that users can:
        1. Pause or stop moving/blinking content
        2. Hide auto-updating information
        3. Control frequency of updates
        4. Essential animations are exempt
        5. Controls are easily accessible
        """
    },
    
    "2.4.1": {
        "id": "2.4.1",
        "title": "Bypass Blocks",
        "level": "A", 
        "description": "Mechanism is available to bypass blocks of content repeated on multiple pages.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Verify bypass mechanisms exist:
        1. Skip links to main content
        2. Skip navigation links
        3. Proper heading structure for navigation
        4. Landmark roles are used appropriately
        5. Skip links are functional and properly positioned
        """
    },
    
    "2.4.2": {
        "id": "2.4.2",
        "title": "Page Titled",
        "level": "A",
        "description": "Pages have titles that describe topic or purpose.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Check that page titles:
        1. Accurately describe the page content or purpose
        2. Are unique within the site (when appropriate)
        3. Are concise and meaningful
        4. Update appropriately for dynamic content
        5. Follow consistent format/structure
        """
    },
    
    "2.4.3": {
        "id": "2.4.3", 
        "title": "Focus Order",
        "level": "A",
        "description": "Components receive focus in an order that preserves meaning and operability.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Test that focus order:
        1. Follows logical sequence (top to bottom, left to right)
        2. Matches visual layout
        3. Groups related elements appropriately
        4. Doesn't skip important interactive elements  
        5. Custom tabindex values are used appropriately
        """
    },
    
    "2.4.4": {
        "id": "2.4.4",
        "title": "Link Purpose (In Context)",
        "level": "A",
        "description": "Purpose of each link can be determined from link text or context.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Ensure link purposes are clear:
        1. Link text describes the destination or function
        2. Context provides additional clarity when needed
        3. Generic terms like 'click here' are avoided
        4. Links to files indicate file type and size
        5. Links that open new windows are identified
        """
    },
    
    "2.4.6": {
        "id": "2.4.6",
        "title": "Headings and Labels",
        "level": "AA",
        "description": "Headings and labels describe topic or purpose.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Verify that:
        1. Headings clearly describe the following content
        2. Form labels clearly describe input purpose
        3. Button labels describe their function
        4. Headings and labels are descriptive, not just decorative
        5. Similar controls have consistent labeling
        """
    },
    
    "3.1.1": {
        "id": "3.1.1",
        "title": "Language of Page",
        "level": "A",
        "description": "Default human language of page can be programmatically determined.",
        "requires_manual_assessment": False,  # Can be automated
        "evaluation_guidelines": """
        Check that:
        1. HTML lang attribute is present on html element
        2. Language code is valid (e.g., 'en', 'es', 'fr')
        3. Language matches the primary page content
        4. Assists screen readers with pronunciation
        """
    },
    
    "3.1.2": {
        "id": "3.1.2", 
        "title": "Language of Parts",
        "level": "AA",
        "description": "Human language of each passage can be programmatically determined.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        For content in different languages:
        1. Foreign phrases have lang attributes
        2. Language changes are properly marked
        3. Only significant passages need marking
        4. Proper names and common loan words are exempt
        5. Language codes are valid and appropriate
        """
    },
    
    "3.2.1": {
        "id": "3.2.1",
        "title": "On Focus",
        "level": "A",
        "description": "Receiving focus does not initiate a change of context.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Ensure focus events don't cause:
        1. Automatic form submission
        2. New windows/tabs opening
        3. Significant content changes
        4. Focus moving to different component
        5. Any other substantial change in context
        """
    },
    
    "3.2.2": {
        "id": "3.2.2",
        "title": "On Input", 
        "level": "A",
        "description": "Changing input settings does not automatically cause change of context.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Test that input changes don't trigger:
        1. Automatic form submission
        2. New window opening
        3. Focus changes to different component
        4. Content reorganization
        5. Provide submit buttons for form submission
        """
    },
    
    "3.3.1": {
        "id": "3.3.1",
        "title": "Error Identification",
        "level": "A",
        "description": "If input error is detected, item in error is identified and error described in text.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        When errors occur, verify:
        1. Specific fields with errors are identified
        2. Error descriptions are provided in text
        3. Errors don't rely solely on color
        4. Error messages are clear and helpful
        5. Users understand what went wrong
        """
    },
    
    "3.3.2": {
        "id": "3.3.2",
        "title": "Labels or Instructions",
        "level": "A", 
        "description": "Labels or instructions are provided when content requires user input.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        Ensure form inputs have:
        1. Clear, descriptive labels
        2. Instructions for expected format
        3. Required field indicators
        4. Help text when needed
        5. Labels are programmatically associated
        """
    },
    
    "4.1.1": {
        "id": "4.1.1",
        "title": "Parsing",
        "level": "A",
        "description": "Content implemented using markup languages has complete start/end tags and proper nesting.",
        "requires_manual_assessment": False,  # Can be automated
        "evaluation_guidelines": """
        HTML validation checks for:
        1. Complete start and end tags
        2. Proper nesting of elements
        3. Unique IDs within page  
        4. Valid attribute usage
        5. Well-formed markup structure
        """
    },
    
    "4.1.2": {
        "id": "4.1.2", 
        "title": "Name, Role, Value",
        "level": "A",
        "description": "Name, role, value can be programmatically determined for UI components.",
        "requires_manual_assessment": True,
        "evaluation_guidelines": """
        For all UI components, verify:
        1. Accessible name is provided (via label, aria-label, etc.)
        2. Role is properly defined (button, link, textbox, etc.)
        3. Current value/state is exposed (checked, expanded, etc.)
        4. State changes are announced to assistive technology
        5. Custom controls have appropriate ARIA attributes
        """
    }
}

# Additional helper functions for categorizing criteria
def get_criteria_by_level(level: str) -> dict:
    """Get all criteria for a specific WCAG level"""
    return {k: v for k, v in WCAG_CRITERIA.items() if v['level'] == level}

def get_manual_criteria() -> dict:
    """Get all criteria that require manual assessment"""
    return {k: v for k, v in WCAG_CRITERIA.items() if v['requires_manual_assessment']}

def get_automated_criteria() -> dict:
    """Get all criteria that can be automated"""
    return {k: v for k, v in WCAG_CRITERIA.items() if not v['requires_manual_assessment']}

# Priority mapping for different types of issues
PRIORITY_MAPPING = {
    'A': {
        'fail': 'critical',
        'warning': 'high',
        'pass': 'low'
    },
    'AA': {
        'fail': 'high', 
        'warning': 'medium',
        'pass': 'low'
    },
    'AAA': {
        'fail': 'medium',
        'warning': 'low', 
        'pass': 'low'
    }
}

def get_priority_for_result(level: str, status: str) -> str:
    """Get priority level based on WCAG level and test result"""
    return PRIORITY_MAPPING.get(level, {}).get(status, 'medium')
