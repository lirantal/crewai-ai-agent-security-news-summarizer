from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import ScrapeWebsiteTool, FileReadTool
from typing import List
from .tools import TableScraperTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SecurityNewsSummary():
    """SecurityNewsSummary crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def cve_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['cve_curator'],
            verbose=True,
            tools=[ScrapeWebsiteTool(), TableScraperTool()]
        )

    @agent
    def cve_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['cve_researcher'],
            verbose=True,
            tools=[ScrapeWebsiteTool()]
        )

    @agent
    def article_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_summarizer'],
            verbose=True,
            tools=[FileReadTool(), ScrapeWebsiteTool()]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def cve_curation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cve_curation_task'],
        )

    @task
    def cve_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['cve_research_task'],
            output_file='cves.md'
        )

    @task
    def article_summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['article_summarization_task'],
            async_execution=True,
            output_file='article_summaries.md',
            tools=[FileReadTool(), ScrapeWebsiteTool()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SecurityNewsSummary crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
