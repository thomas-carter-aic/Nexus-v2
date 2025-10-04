package com.platform.user.adapters.inbound;
import org.springframework.web.bind.annotation.*;
import java.time.Instant;
import java.util.Map;
@RestController
@RequestMapping("/users")
public class UserController {
  @PostMapping("/create")
  public Map<String,String> create(@RequestBody Map<String,String> body){
    String id = body.getOrDefault("id", "u-"+Instant.now().toEpochMilli());
    String email = body.getOrDefault("email","unknown@example.com");
    String evt = String.format("{\"type\":\"UserCreated\",\"payload\":{\"userId\":\"%s\",\"email\":\"%s\",\"createdAt\":\"%s\"}}", id, email, Instant.now().toString());
    String kafka = System.getenv("KAFKA_BOOTSTRAP");
    if(kafka!=null && !kafka.isBlank()){
      System.out.println("[KAFKA-PLACEHOLDER] would publish to Kafka: " + evt);
    } else {
      System.out.println(evt);
    }
    return Map.of("status","created","userId",id);
  }
}
