import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Any
import os

WCAG_LEVEL_TAGS = {
    "A": "wcag2a",
    "AA": "wcag2aa",
    "AAA": "wcag2aaa"
}

class AccessibilityChecker:
    """
    Handles automated accessibility testing using axe-core and Selenium
    """
    
    def __init__(self):
        self.driver = None
    
    def _setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"Failed to initialize Chrome driver: {e}")
            return False
    
    def _inject_axe_core(self):
        """Inject axe-core JavaScript library into the page"""
        # axe.min.jsをローカルから読み込む
        with open(os.path.join(os.path.dirname(__file__), "axe.min.js"), "r", encoding="utf-8") as f:
            axe_script = f.read()
        self.driver.execute_script(axe_script)
        # axe-coreがロードされるまで待機
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return typeof axe !== 'undefined';")
        )
        # axe-coreが本当にロードされたか確認
        axe_type = self.driver.execute_script("return typeof axe;")
        print(f"axe type: {axe_type}")  # 'object' であればOK、'undefined'ならNG
    
    def run_axe_core_analysis(self, url: str, wcag_levels: list = None) -> Dict[str, Any]:
        """
        Run axe-core accessibility analysis on the given URL
        
        Args:
            url: The URL to analyze
            wcag_levels: List of WCAG levels to analyze
            
        Returns:
            Dictionary containing axe-core results
        """
        if not self._setup_driver():
            raise Exception("Failed to setup WebDriver")
        
        try:
            # Navigate to the URL
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Inject axe-core
            self._inject_axe_core()
            
            # WCAGレベルをタグに変換
            if wcag_levels:
                tags = [WCAG_LEVEL_TAGS[level] for level in wcag_levels if level in WCAG_LEVEL_TAGS]
            else:
                tags = ["wcag2a", "wcag2aa"]  # デフォルト
            
            axe_options = {
                "runOnly": {
                    "type": "tag",
                    "values": tags
                }
            }
            
            # Run axe-core analysis with options
            axe_results = self.driver.execute_async_script("""
                const callback = arguments[arguments.length - 1];
                axe.run(document, %s).then(results => callback(results)).catch(err => callback({error: err.toString()}));
            """ % json.dumps(axe_options))
            
            # Process and clean results
            if axe_results is None:
                raise Exception("axe.run did not return any results (None). JavaScript execution may have failed.")
            return self._process_axe_results(axe_results)
            
        except Exception as e:
            raise Exception(f"Error during axe-core analysis: {str(e)}")
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _process_axe_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process and clean axe-core results"""
        if 'error' in results:
            raise Exception(f"axe-core error: {results['error']}")
        
        processed = {
            'violations': [],
            'passes': [],
            'incomplete': [],
            'inapplicable': []
        }
        
        for category in processed.keys():
            if category in results:
                for item in results[category]:
                    processed_item = {
                        'id': item.get('id'),
                        'description': item.get('description'),
                        'help': item.get('help'),
                        'helpUrl': item.get('helpUrl'),
                        'impact': item.get('impact'),
                        'tags': item.get('tags', []),
                        'nodes': []
                    }
                    
                    # Process nodes (affected elements)
                    for node in item.get('nodes', []):
                        processed_node = {
                            'target': node.get('target', []),
                            'html': node.get('html', ''),
                            'failureSummary': node.get('failureSummary', ''),
                            'impact': node.get('impact')
                        }
                        processed_item['nodes'].append(processed_node)
                    
                    processed[category].append(processed_item)
        
        return processed
    
    def get_page_content(self, url: str) -> Dict[str, Any]:
        """
        Extract page content for AI analysis
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing page content and metadata
        """
        try:
            # Get page with requests first for basic content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key content for AI analysis
            content = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'headings': self._extract_headings(soup),
                'images': self._extract_images(soup),
                'links': self._extract_links(soup),
                'forms': self._extract_forms(soup),
                'text_content': soup.get_text()[:5000],  # First 5000 chars
                'html_structure': str(soup)[:10000],  # First 10000 chars of HTML
                'meta_tags': self._extract_meta_tags(soup)
            }
            
            return content
            
        except Exception as e:
            raise Exception(f"Error extracting page content: {str(e)}")
    
    def _extract_headings(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract heading structure from the page"""
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip(),
                    'tag': heading.name
                })
        return headings
    
    def _extract_images(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract image information for accessibility analysis"""
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'has_alt': bool(img.get('alt'))
            })
        return images
    
    def _extract_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract link information for accessibility analysis"""
        links = []
        for link in soup.find_all('a'):
            links.append({
                'href': link.get('href', ''),
                'text': link.get_text().strip(),
                'title': link.get('title', ''),
                'has_text': bool(link.get_text().strip())
            })
        return links
    
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract form information for accessibility analysis"""
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', ''),
                'inputs': []
            }
            
            for input_elem in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'type': input_elem.get('type', ''),
                    'name': input_elem.get('name', ''),
                    'id': input_elem.get('id', ''),
                    'label': '',
                    'has_label': False
                }
                
                # Check for associated label
                if input_elem.get('id'):
                    label = soup.find('label', {'for': input_elem.get('id')})
                    if label:
                        input_data['label'] = label.get_text().strip()
                        input_data['has_label'] = True
                
                form_data['inputs'].append(input_data)
            
            forms.append(form_data)
        
        return forms
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta tags for accessibility analysis"""
        meta_tags = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content:
                meta_tags[name] = content
        
        return meta_tags
