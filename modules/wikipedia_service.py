#!/usr/bin/env python3
"""
Wikipedia Service Module
Searches Wikipedia and provides summaries
"""

import wikipedia
import requests
from typing import Optional, List
import re

class WikipediaService:
    def __init__(self):
        """Initialize Wikipedia service"""
        # Set language to English
        wikipedia.set_lang("en")
        
    def search_wikipedia(self, query: str, sentences: int = 3) -> str:
        """
        Search Wikipedia and return summary
        
        Args:
            query: Search query
            sentences: Number of sentences to return
            
        Returns:
            str: Wikipedia summary or error message
        """
        try:
            print(f"Searching Wikipedia for: {query}")
            
            # Search for pages
            search_results = wikipedia.search(query, results=5)
            
            if not search_results:
                return f"I couldn't find any Wikipedia articles about '{query}'."
            
            # Try to get the page for the first result
            for result in search_results:
                try:
                    page = wikipedia.page(result)
                    summary = wikipedia.summary(result, sentences=sentences)
                    
                    # Clean up the summary
                    summary = self._clean_summary(summary)
                    
                    return f"According to Wikipedia: {summary}"
                    
                except wikipedia.DisambiguationError as e:
                    # If there are multiple options, try the first one
                    try:
                        page = wikipedia.page(e.options[0])
                        summary = wikipedia.summary(e.options[0], sentences=sentences)
                        summary = self._clean_summary(summary)
                        return f"According to Wikipedia: {summary}"
                    except:
                        continue
                        
                except wikipedia.PageError:
                    # Page doesn't exist, try next result
                    continue
                    
                except Exception as e:
                    print(f"Error with result '{result}': {e}")
                    continue
            
            return f"I found some results for '{query}' but couldn't retrieve the content. Please try a more specific search."
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return f"I encountered an error while searching Wikipedia for '{query}'. Please try again."
    
    def _clean_summary(self, summary: str) -> str:
        """Clean up Wikipedia summary text"""
        # Remove citation markers like [1], [2], etc.
        summary = re.sub(r'\[\d+\]', '', summary)
        
        # Remove extra whitespace
        summary = ' '.join(summary.split())
        
        # Ensure it ends with proper punctuation
        if summary and not summary.endswith(('.', '!', '?')):
            summary += '.'
        
        return summary
    
    def get_page_url(self, query: str) -> Optional[str]:
        """
        Get Wikipedia page URL for a query
        
        Args:
            query: Search query
            
        Returns:
            str: Wikipedia page URL or None
        """
        try:
            search_results = wikipedia.search(query, results=1)
            if search_results:
                page = wikipedia.page(search_results[0])
                return page.url
        except:
            pass
        return None
    
    def search_and_open(self, query: str) -> str:
        """
        Search Wikipedia and provide summary with option to open page
        
        Args:
            query: Search query
            
        Returns:
            str: Summary with URL information
        """
        try:
            summary = self.search_wikipedia(query, sentences=2)
            url = self.get_page_url(query)
            
            if url:
                # For now, just mention the URL exists
                # In a full implementation, you could open it in browser
                summary += f" You can read more at the Wikipedia page."
            
            return summary
            
        except Exception as e:
            print(f"Search and open error: {e}")
            return f"I couldn't search Wikipedia for '{query}' right now."

# Test function
def test_wikipedia_service():
    """Test the Wikipedia service"""
    print("Testing Wikipedia Service")
    print("=" * 30)
    
    wiki = WikipediaService()
    
    test_queries = [
        "Python programming language",
        "Artificial Intelligence",
        "Solar System",
        "Nonexistent Topic XYZ123"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Searching for: '{query}'")
        result = wiki.search_wikipedia(query, sentences=2)
        print(f"Result: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_wikipedia_service()