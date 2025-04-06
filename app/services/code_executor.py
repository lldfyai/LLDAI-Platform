import os
from config import LANGUAGE_CONFIG, UPLOAD_DIR
import docker
from io import BytesIO
import tarfile
from models.CodeExecResponseModel import CodeExecResponseModel
from models.ErrorResponseModel import ErrorResponseModel, ErrorType, Errors
from enum import Enum

class StateEnum(Enum):
    COMPLETED = "Completed"
    FAILURE = "Failure"

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
    def execute_code_in_docker(self, submission_id, problem_id, language, submission_folder):
        # Ensure the Docker image is built
        abs_submission_folder = os.path.abspath(submission_folder)
        output_folder = os.path.join(abs_submission_folder, "output")
        os.makedirs(output_folder, exist_ok=True)
        image_name, error = self.build_docker_image(language, submission_folder)
        if not image_name:
            return {"state": StateEnum.FAILURE.value, "output": ErrorResponseModel.populate_response_model(ErrorType.SYSTEM_ERROR, str(error))}
        try:
            # Run the container with the user-submitted code files
            container = self.client.containers.run(
                image=image_name, 
                working_dir="/app",
                detach=True,
                stdout=True,
                stderr=True
            )
            container.wait()  # Wait for the container to finish

            #Copy compile log from the container to the host
            file_name = "compile.log"
            src_path = f"/app/output/{file_name}"
            dest_path = os.path.join(output_folder, file_name)
            self.copy_file_from_container(container.id, src_path, dest_path)
            if os.path.exists(dest_path):
                with open(dest_path, "r") as file:
                    error_msg = file.read().strip()
                if error_msg:
                    # Compilation error occurred
                    return {"state": StateEnum.FAILURE.value, "output": ErrorResponseModel.populate_response_model(Errors.COMPILATION_ERROR.status_code, error_msg, Errors.COMPILATION_ERROR.error_type)}    


            # Copy generated files from the container to the host
            generated_files = ["results.properties", "stdout.txt", "stderr.txt"]
            for file_name in generated_files:
                src_path = f"/app/output/{file_name}"
                dest_path = os.path.join(output_folder, file_name)
                self.copy_file_from_container(container.id, src_path, dest_path)

            
            container.remove()  # Remove the container after copying files
            response = self.generate_response_model(submission_id, problem_id, language, output_folder)
            return {"state": StateEnum.COMPLETED.value, "output": response}
        except docker.errors.ContainerError as e:
            return {"state": StateEnum.FAILURE.value, "output": ErrorResponseModel.populate_response_model(Errors.SYSTEM_ERROR.status_code, str(e.stderr.decode()), Errors.SYSTEM_ERROR.error_type)}
        except Exception as e:
            return {"state": StateEnum.FAILURE.value, "output": ErrorResponseModel.populate_response_model(Errors.SYSTEM_ERROR.status_code, str(e), Errors.SYSTEM_ERROR.error_type)}

    def copy_file_from_container(self, container_id, src_path, dest_path):
        container = self.client.containers.get(container_id)
        tar_stream, _ = container.get_archive(src_path)
        tar_data = BytesIO()
        for chunk in tar_stream:
            tar_data.write(chunk)
        tar_data.seek(0)
        with tarfile.open(fileobj=tar_data) as tar:
            tar.extractall(path=os.path.dirname(dest_path))

    def generate_response_model(self, submission_id, problem_id, lang, output_folder):
      results_file = os.path.join(output_folder, "results.properties")
      stdout_file = os.path.join(output_folder, "stdout.txt")
      stderr_file = os.path.join(output_folder, "stderr.txt")
    
      results = {}
      stdout = ""
      stderr = ""

      if os.path.exists(results_file):
        with open(results_file, "r") as file:
            results = dict(line.strip().split('=', 1) for line in file if '=' in line)

      if os.path.exists(stdout_file):
        with open(stdout_file, "r") as file:
            stdout = file.read()
    
      if os.path.exists(stderr_file):
        with open(stderr_file, "r") as file:
            stderr = file.read()

      response = CodeExecResponseModel.populate_response_model(
        status_code=200,
        lang=lang,
        run_success=True,
        exec_runtime=results.get("execTime", "N/A"),
        memory="N/A",
        problem_id=problem_id,
        finished=True,
        total_correct=int(results.get("testsPassed", 0)),
        total_testcases=int(results.get("totalTestCases", 0)),
        submission_id=submission_id,
        status_msg="Execution completed",
        evaluation_state="Completed",
        failed_testcase=results.get("failedTestCaseNum"),
        expected_output=results.get("expectedOutput"),
        actual_output=results.get("actualOutput"),
        error_msg="None"
      )

      return response        

    