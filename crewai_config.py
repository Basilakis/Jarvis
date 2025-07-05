"""
CrewAI Configuration and Integration Module
Integrates CrewAI with the Jarvis AI system and roo-commander ecosystem
"""

import os
from typing import Dict, List, Optional, Any
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    FileReadTool,
    DirectoryReadTool,
    CodeDocsSearchTool,
    YoutubeChannelSearchTool,
    YoutubeVideoSearchTool,
    GithubSearchTool,
    TXTSearchTool,
    JSONSearchTool,
    MDXSearchTool,
    PDFSearchTool,
    DOCXSearchTool,
    CSVSearchTool,
    XMLSearchTool,
    ScrapeWebsiteTool,
    SeleniumScrapingTool,
    PGSearchTool,
    MySQLSearchTool,
    DirectorySearchTool,
    FirecrawlCrawlWebsiteTool,
    FirecrawlScrapeWebsiteTool,
    FirecrawlSearchTool
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JarvisCrewAIConfig:
    """Configuration class for CrewAI integration with Jarvis AI system"""
    
    def __init__(self):
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'google': os.getenv('GOOGLE_AI_API_KEY'),
            'serper': os.getenv('SERPER_API_KEY'),
            'firecrawl': os.getenv('FIRECRAWL_API_KEY')
        }
        
        self.model_config = {
            'provider': os.getenv('CREWAI_MODEL_PROVIDER', 'openai'),
            'model': os.getenv('CREWAI_MODEL_NAME', 'gpt-4'),
            'temperature': 0.7,
            'max_tokens': 4000
        }
        
        self.workspace_path = os.getcwd()
        self.roo_path = os.path.join(self.workspace_path, '.roo')
        self.ruru_path = os.path.join(self.workspace_path, '.ruru')
        
    def get_available_tools(self) -> List[BaseTool]:
        """Get all available CrewAI tools configured for Jarvis system"""
        tools = []
        
        # File and directory tools
        tools.extend([
            FileReadTool(),
            DirectoryReadTool(),
            DirectorySearchTool(),
            TXTSearchTool(),
            JSONSearchTool(),
            MDXSearchTool(),
            PDFSearchTool(),
            DOCXSearchTool(),
            CSVSearchTool(),
            XMLSearchTool()
        ])
        
        # Web scraping and search tools
        if self.api_keys.get('serper'):
            tools.append(SerperDevTool())
        
        tools.extend([
            WebsiteSearchTool(),
            ScrapeWebsiteTool(),
            SeleniumScrapingTool()
        ])
        
        # Firecrawl tools (if API key available)
        if self.api_keys.get('firecrawl'):
            tools.extend([
                FirecrawlCrawlWebsiteTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlSearchTool()
            ])
        
        # Code and documentation tools
        tools.extend([
            CodeDocsSearchTool(),
            GithubSearchTool()
        ])
        
        # YouTube tools
        tools.extend([
            YoutubeChannelSearchTool(),
            YoutubeVideoSearchTool()
        ])
        
        # Database tools (if configured)
        if os.getenv('DATABASE_URL'):
            if 'postgresql' in os.getenv('DATABASE_URL', ''):
                tools.append(PGSearchTool())
            elif 'mysql' in os.getenv('DATABASE_URL', ''):
                tools.append(MySQLSearchTool())
        
        return tools

class JarvisCrewAIAgents:
    """Predefined CrewAI agents for Jarvis AI system"""
    
    def __init__(self, config: JarvisCrewAIConfig):
        self.config = config
        self.tools = config.get_available_tools()
    
    def create_roo_commander_agent(self) -> Agent:
        """Create an agent that interfaces with roo-commander system"""
        return Agent(
            role='Roo Commander Interface',
            goal='Interface with the roo-commander ecosystem and coordinate AI agent tasks',
            backstory="""You are an expert AI agent coordinator that understands the roo-commander 
            ecosystem. You can read and interpret TOML+Markdown files, understand MDTM workflows, 
            and coordinate with specialized AI modes.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            memory=True
        )
    
    def create_code_analyst_agent(self) -> Agent:
        """Create an agent specialized in code analysis"""
        return Agent(
            role='Code Analyst',
            goal='Analyze code structure, patterns, and provide insights for development',
            backstory="""You are an expert code analyst with deep knowledge of multiple 
            programming languages, design patterns, and software architecture. You can 
            analyze codebases and provide actionable insights.""",
            tools=[tool for tool in self.tools if any(keyword in str(type(tool)) for keyword in 
                  ['File', 'Directory', 'Code', 'TXT', 'JSON', 'XML'])],
            verbose=True,
            max_iter=3,
            memory=True
        )
    
    def create_research_agent(self) -> Agent:
        """Create an agent specialized in research and information gathering"""
        return Agent(
            role='Research Specialist',
            goal='Conduct thorough research and gather relevant information from various sources',
            backstory="""You are an expert researcher with the ability to find, analyze, 
            and synthesize information from multiple sources including web content, 
            documentation, and databases.""",
            tools=[tool for tool in self.tools if any(keyword in str(type(tool)) for keyword in 
                  ['Search', 'Scrape', 'Website', 'Youtube', 'Github', 'Firecrawl'])],
            verbose=True,
            max_iter=4,
            memory=True
        )
    
    def create_documentation_agent(self) -> Agent:
        """Create an agent specialized in documentation tasks"""
        return Agent(
            role='Documentation Specialist',
            goal='Create, update, and maintain high-quality documentation',
            backstory="""You are an expert technical writer who specializes in creating 
            clear, comprehensive documentation. You understand various documentation 
            formats including Markdown, TOML+MD, and can work with the roo-commander 
            documentation standards.""",
            tools=[tool for tool in self.tools if any(keyword in str(type(tool)) for keyword in 
                  ['File', 'Directory', 'TXT', 'MDX', 'PDF', 'DOCX'])],
            verbose=True,
            max_iter=3,
            memory=True
        )

class JarvisCrewAITasks:
    """Predefined CrewAI tasks for common Jarvis operations"""
    
    @staticmethod
    def create_roo_analysis_task(agent: Agent) -> Task:
        """Create a task to analyze the roo-commander ecosystem"""
        return Task(
            description="""Analyze the current roo-commander ecosystem structure:
            1. Read and understand the .roo and .ruru directory structures
            2. Identify key rules, modes, and workflows
            3. Assess the current configuration and capabilities
            4. Provide recommendations for optimization or improvements
            """,
            agent=agent,
            expected_output="Comprehensive analysis report of the roo-commander ecosystem with actionable recommendations"
        )
    
    @staticmethod
    def create_code_integration_task(agent: Agent, integration_type: str) -> Task:
        """Create a task for code integration"""
        return Task(
            description=f"""Integrate {integration_type} into the Jarvis AI system:
            1. Analyze the current codebase structure
            2. Identify integration points and dependencies
            3. Create or modify configuration files as needed
            4. Ensure compatibility with existing roo-commander workflows
            5. Document the integration process and usage
            """,
            agent=agent,
            expected_output=f"Complete {integration_type} integration with documentation and configuration files"
        )
    
    @staticmethod
    def create_documentation_task(agent: Agent, topic: str) -> Task:
        """Create a documentation task"""
        return Task(
            description=f"""Create comprehensive documentation for {topic}:
            1. Research the topic thoroughly
            2. Understand the context within the Jarvis AI system
            3. Create structured documentation using TOML+MD format
            4. Include examples, usage patterns, and best practices
            5. Ensure consistency with existing documentation standards
            """,
            agent=agent,
            expected_output=f"Complete documentation for {topic} in TOML+MD format with examples and best practices"
        )

class JarvisCrewAIOrchestrator:
    """Main orchestrator for CrewAI operations in Jarvis system"""
    
    def __init__(self):
        self.config = JarvisCrewAIConfig()
        self.agents = JarvisCrewAIAgents(self.config)
        self.tasks = JarvisCrewAITasks()
    
    def create_integration_crew(self, integration_type: str) -> Crew:
        """Create a crew for handling integrations"""
        # Create agents
        commander_agent = self.agents.create_roo_commander_agent()
        code_agent = self.agents.create_code_analyst_agent()
        research_agent = self.agents.create_research_agent()
        doc_agent = self.agents.create_documentation_agent()
        
        # Create tasks
        analysis_task = self.tasks.create_roo_analysis_task(commander_agent)
        integration_task = self.tasks.create_code_integration_task(code_agent, integration_type)
        documentation_task = self.tasks.create_documentation_task(doc_agent, f"{integration_type} Integration")
        
        # Create crew
        return Crew(
            agents=[commander_agent, code_agent, research_agent, doc_agent],
            tasks=[analysis_task, integration_task, documentation_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    def create_research_crew(self, research_topic: str) -> Crew:
        """Create a crew for research tasks"""
        research_agent = self.agents.create_research_agent()
        doc_agent = self.agents.create_documentation_agent()
        
        research_task = Task(
            description=f"""Research {research_topic} comprehensively:
            1. Gather information from multiple sources
            2. Analyze current trends and best practices
            3. Identify relevant tools and technologies
            4. Assess compatibility with Jarvis AI system
            """,
            agent=research_agent,
            expected_output=f"Comprehensive research report on {research_topic}"
        )
        
        documentation_task = self.tasks.create_documentation_task(doc_agent, f"{research_topic} Research")
        
        return Crew(
            agents=[research_agent, doc_agent],
            tasks=[research_task, documentation_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    def execute_integration(self, integration_type: str) -> Dict[str, Any]:
        """Execute an integration workflow"""
        crew = self.create_integration_crew(integration_type)
        result = crew.kickoff()
        
        return {
            'integration_type': integration_type,
            'status': 'completed',
            'result': result,
            'crew_id': id(crew)
        }
    
    def execute_research(self, research_topic: str) -> Dict[str, Any]:
        """Execute a research workflow"""
        crew = self.create_research_crew(research_topic)
        result = crew.kickoff()
        
        return {
            'research_topic': research_topic,
            'status': 'completed',
            'result': result,
            'crew_id': id(crew)
        }

# Initialize the orchestrator
jarvis_crew_orchestrator = JarvisCrewAIOrchestrator()

# Export main classes and functions
__all__ = [
    'JarvisCrewAIConfig',
    'JarvisCrewAIAgents', 
    'JarvisCrewAITasks',
    'JarvisCrewAIOrchestrator',
    'jarvis_crew_orchestrator'
]