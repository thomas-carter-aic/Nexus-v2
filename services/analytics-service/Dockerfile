FROM eclipse-temurin:21
WORKDIR /app
COPY build.gradle .
COPY src ./src
RUN ./gradlew build
CMD ["java", "-jar", "build/libs/analytics-service-1.0.0.jar"]
