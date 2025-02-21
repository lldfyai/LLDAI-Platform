import docker
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class CodeExecutor:
    def __init__(self):
        self.client = self._initialize_docker_client()

    def _initialize_docker_client(self):
        try:
            client = docker.DockerClient(
                base_url='unix://var/run/docker.sock',
                version='auto',
                timeout=10
            )
            self._verify_connection(client)
            return client
        except docker.errors.DockerException as e:
            logger.error(f"Docker connection failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Docker service unavailable - check container permissions"
            )

    def _verify_connection(self, client):
        try:
            info = client.info()
            logger.info(f"Connected to Docker {info['ServerVersion']}")
        except Exception as e:
            logger.error(f"Docker verification failed: {str(e)}")
            raise

    def execute_code_in_docker(self, job_id, language, user_folder):
        try:
            return self._run_container(job_id, language, user_folder)
        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            return {"error": "Code execution failed"}

    def _run_container(self, job_id, language, user_folder):
        container = self.client.containers.run(
            image=f"code-executor-{language}",
            command=f"./execute {job_id}",
            volumes={
                user_folder: {'bind': '/code', 'mode': 'rw'},
                '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'ro'}
            },
            mem_limit='512m',
            cpu_shares=512,
            auto_remove=True,
            network_mode='none',
            detach=True
        )
        return {"container_id": container.id}