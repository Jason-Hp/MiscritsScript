FROM eclipse-temurin:17-jdk-jammy AS build
WORKDIR /workspace/app

COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN ./mvnw -q -B -DskipTests dependency:go-offline

COPY src/ src/
RUN ./mvnw -q -B -DskipTests package

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /workspace/app/target/*.jar /app/consumer.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/consumer.jar"]
