from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
import os

# Define custom callback handler

@CrewBase
class ProjectAiver2():
    """ProjectAiver2"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def Writer(self) -> Agent:
        return Agent(
            config=self.agents_config['Writer'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['Writing_task'],
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiProject crew"""
        # Use instance of CustomCallbackHandler
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
