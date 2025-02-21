# app/services/code_executor.py
import docker
import os
from fastapi import HTTPException

class CodeExecutor:
    def __init__(self):
        self.client = self._get_docker_client()

    def _get_docker_client(self):
        try:
            # Try Docker socket first
            client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            client.ping()
            return client
        except docker.errors.DockerException:
            try:
                # Fallback to TCP
                client = docker.DockerClient(base_url='tcp://localhost:2375')
                client.ping()
                return client
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Docker connection failed: {str(e)}"
                )

    def execute_code_in_docker(self, job_id, language, user_folder):
        try:
            return self._run_container(job_id, language, user_folder)
        except Exception as e:
            return {"error": str(e)}

    def _run_container(self, job_id, language, user_folder):
        # Add container cleanup and resource limits
        container = self.client.containers.run(
            image=f"code-executor-{language}",
            command=f"./execute {job_id}",
            volumes={user_folder: {'bind': '/code', 'mode': 'rw'}},
            mem_limit='512m',
            cpu_shares=512,
            auto_remove=True,
            network_mode='none'
        )
        return {"output": container.logs().decode()}