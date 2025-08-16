#!/usr/bin/env python3
"""
News Service Module
Fetches news from various sources
"""

import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import re

class NewsService:
    def __init__(self):
        """Initialize news service"""
        # Free RSS feeds that don't require API keys
        self.news_sources = {
            'general': [
                {'name': 'BBC News', 'url': 'http://feeds.bbci.co.uk/news/rss.xml'},
                {'name': 'Reuters', 'url': 'http://feeds.reuters.com/reuters/topNews'},
                {'name': 'Associated Press', 'url': 'https://feeds.apnews.com/rss/apf-topnews'},
            ],
            'tech': [
                {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/'},
                {'name': 'Ars Technica', 'url': 'http://feeds.arstechnica.com/arstechnica/index'},
                {'name': 'The Verge', 'url': 'https://www.theverge.com/rss/index.xml'},
            ],
            'science': [
                {'name': 'Science Daily', 'url': 'https://www.sciencedaily.com/rss/all.xml'},
                {'name': 'NASA News', 'url': 'https://www.nasa.gov/rss/dyn/breaking_news.rss'},
            ]
        }
    
    def get_latest_news(self, category: str = 'general', count: int = 3) -> str:
        """
        Get latest news headlines
        
        Args:
            category: News category ('general', 'tech', 'science')
            count: Number of headlines to return
            
        Returns:
            str: News summary
        """
        try:
            if category not in self.news_sources:
                category = 'general'
            
            print(f"Fetching {category} news...")
            
            all_articles = []
            
            # Try each source in the category
            for source in self.news_sources[category]:
                try:
                    articles = self._fetch_rss_feed(source['url'], source['name'])
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"Error fetching from {source['name']}: {e}")
                    continue
            
            if not all_articles:
                return "I couldn't fetch the latest news right now. Please check your internet connection."
            
            # Sort by date (most recent first) and take top articles
            all_articles.sort(key=lambda x: x.get('published', ''), reverse=True)
            top_articles = all_articles[:count]
            
            # Format the news
            news_text = f"Here are the latest {category} news headlines: "
            
            for i, article in enumerate(top_articles, 1):
                title = article['title']
                source = article['source']
                news_text += f"{i}. {title} from {source}. "
            
            return news_text
            
        except Exception as e:
            print(f"News service error: {e}")
            return "I encountered an error while fetching the news. Please try again later."
    
    def _fetch_rss_feed(self, url: str, source_name: str) -> List[Dict]:
        """
        Fetch articles from RSS feed
        
        Args:
            url: RSS feed URL
            source_name: Name of the news source
            
        Returns:
            List of article dictionaries
        """
        try:
            # Parse RSS feed
            feed = feedparser.parse(url)
            
            articles = []
            
            for entry in feed.entries[:5]:  # Get top 5 from each source
                article = {
                    'title': self._clean_title(entry.title),
                    'source': source_name,
                    'published': getattr(entry, 'published', ''),
                    'summary': self._clean_summary(getattr(entry, 'summary', ''))
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"RSS feed error for {source_name}: {e}")
            return []
    
    def _clean_title(self, title: str) -> str:
        """Clean up news title"""
        # Remove HTML tags
        title = re.sub(r'<[^>]+>', '', title)
        
        # Remove extra whitespace
        title = ' '.join(title.split())
        
        return title
    
    def _clean_summary(self, summary: str) -> str:
        """Clean up news summary"""
        # Remove HTML tags
        summary = re.sub(r'<[^>]+>', '', summary)
        
        # Remove extra whitespace
        summary = ' '.join(summary.split())
        
        # Limit length
        if len(summary) > 200:
            summary = summary[:200] + "..."
        
        return summary
    
    def search_news(self, topic: str, count: int = 3) -> str:
        """
        Search for news about a specific topic
        
        Args:
            topic: Topic to search for
            count: Number of articles to return
            
        Returns:
            str: News search results
        """
        try:
            print(f"Searching news for: {topic}")
            
            # Get articles from all categories
            all_articles = []
            
            for category in self.news_sources:
                for source in self.news_sources[category]:
                    try:
                        articles = self._fetch_rss_feed(source['url'], source['name'])
                        all_articles.extend(articles)
                    except:
                        continue
            
            # Filter articles that mention the topic
            topic_lower = topic.lower()
            relevant_articles = []
            
            for article in all_articles:
                title_lower = article['title'].lower()
                summary_lower = article.get('summary', '').lower()
                
                if topic_lower in title_lower or topic_lower in summary_lower:
                    relevant_articles.append(article)
            
            if not relevant_articles:
                return f"I couldn't find any recent news about '{topic}'. Try a different search term."
            
            # Take top results
            top_articles = relevant_articles[:count]
            
            news_text = f"Here's what I found about '{topic}': "
            
            for i, article in enumerate(top_articles, 1):
                title = article['title']
                source = article['source']
                news_text += f"{i}. {title} from {source}. "
            
            return news_text
            
        except Exception as e:
            print(f"News search error: {e}")
            return f"I encountered an error while searching for news about '{topic}'."
    
    def get_news_summary(self) -> str:
        """Get a brief news summary from multiple categories"""
        try:
            summary_parts = []
            
            # Get one headline from each category
            for category in ['general', 'tech', 'science']:
                try:
                    articles = []
                    for source in self.news_sources[category][:1]:  # Just first source
                        articles.extend(self._fetch_rss_feed(source['url'], source['name']))
                    
                    if articles:
                        top_article = articles[0]
                        summary_parts.append(f"{category.title()}: {top_article['title']}")
                        
                except:
                    continue
            
            if summary_parts:
                return "Here's a quick news summary: " + ". ".join(summary_parts) + "."
            else:
                return "I couldn't fetch a news summary right now."
                
        except Exception as e:
            print(f"News summary error: {e}")
            return "I encountered an error while getting the news summary."

# Test function
def test_news_service():
    """Test the news service"""
    print("Testing News Service")
    print("=" * 30)
    
    news = NewsService()
    
    print("1. General news:")
    general_news = news.get_latest_news('general', 2)
    print(f"   {general_news}")
    
    print("\n2. Tech news:")
    tech_news = news.get_latest_news('tech', 2)
    print(f"   {tech_news}")
    
    print("\n3. News summary:")
    summary = news.get_news_summary()
    print(f"   {summary}")

if __name__ == "__main__":
    test_news_service()