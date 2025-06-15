from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
from crewai.tools import BaseTool

class TableScraperTool(BaseTool):
    name: str = "table_scraper"
    description: str = "Scrapes table data from a webpage, extracting rows, links, and other relevant information"

    def _run(self, url: str) -> List[Dict[str, Any]]:
        """
        Scrapes table data from the given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            List of dictionaries containing table row data
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all table rows
            rows = soup.find_all('tr', class_='table__row')
            table_data = []
            
            for row in rows:
                row_data = {}
                
                # Extract severity
                severity_elem = row.find('li', class_='severity__item')
                if severity_elem:
                    row_data['severity'] = severity_elem.get('class', [''])[0].replace('severity__item--', '')
                
                # Extract vulnerability title and link
                title_link = row.find('a', class_='anchor--underline')
                if title_link:
                    row_data['title'] = title_link.text.strip()
                    row_data['vuln_link'] = title_link.get('href', '')
                
                # Extract package name and link
                package_link = row.find('a', attrs={'data-snyk-test-package-manager': True})
                if package_link:
                    row_data['package_name'] = package_link.text.strip()
                    row_data['package_link'] = package_link.get('href', '')
                
                # Extract version ranges
                version_spans = row.find_all('span', class_='vulns-table__semver')
                if version_spans:
                    row_data['version_ranges'] = [span.text.strip() for span in version_spans]
                
                # Extract package manager and date
                package_manager = row.find('span', attrs={'type': True})
                if package_manager:
                    row_data['package_manager'] = package_manager.get('type', '')
                    row_data['published_date'] = package_manager.get('published', '')
                
                if row_data:  # Only add if we found some data
                    table_data.append(row_data)
            
            return table_data
            
        except Exception as e:
            return [{"error": f"Failed to scrape table data: {str(e)}"}]

    async def _arun(self, url: str) -> List[Dict[str, Any]]:
        """Async implementation of the tool"""
        return self._run(url) 