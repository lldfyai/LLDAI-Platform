import os
from config import LANGUAGE_CONFIG, UPLOAD_DIR
import docker

class CodeExecutor:
    def __init__(self):
        self.client = docker.from_env()
        
    """Builds a Docker image for the specified language."""    
    def build_docker_image(self, language, submission_folder): 
        config = LANGUAGE_CONFIG.get(language)
        if not config:
            return None, "Unsupported language"
        
        image_name = config["image"]
        dockerfile_path = config["dockerfile"]
        try:
            print(f"Building Docker image for {language}...")
            self.client.images.build(path=".", dockerfile=dockerfile_path, tag=image_name,  buildargs={"JOB_FOLDER": submission_folder})
            print(f"Docker image {image_name} built successfully!")
            return image_name, None

        except Exception as e:
            return None, f"Error building Docker image: {str(e)}"

    """Runs Java code inside the dynamically built Docker container."""        
    def execute_code_in_docker(self, submission_id, language, submission_folder):
        # Ensure the Docker image is built
        abs_submission_folder = os.path.abspath(submission_folder)
        image_name, error = self.build_docker_image(language, submission_folder)
        if not image_name:
            return {"status": "Error", "output": error}
        try:
            # Run the container with the user-submitted code files
            container = self.client.containers.run(
                image=image_name, 
                working_dir="/app",
                remove=True,
                stdout=True,
                stderr=True
            )
            return {"status": "Success", "output": container.decode()}
        except docker.errors.ContainerError as e:
            return {"status": "Execution Failed", "output": str(e.stderr.decode())}
        except Exception as e:
            return {"status": "Error", "output": str(e)}
