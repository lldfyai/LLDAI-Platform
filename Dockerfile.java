FROM openjdk:17
WORKDIR /app
ARG JOB_FOLDER
COPY ${JOB_FOLDER} /app
RUN javac *.java
CMD ["java", "Main"]