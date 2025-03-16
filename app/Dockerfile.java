FROM openjdk:17
WORKDIR /app
ARG JOB_FOLDER
COPY ${JOB_FOLDER} /app
RUN javac *.java > /app/output/compile.log 2>&1 || true
CMD ["java", "Main"]