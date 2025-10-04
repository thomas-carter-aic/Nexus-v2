import openapi_generator
import requests

def generate_openapi_client(spec_path, output_dir):
    # Generate client using openapi-generator
    openapi_generator.generate(spec_path, output_dir, "python")
    # Enhance with xAI API (placeholder)
    response = requests.post(
        "https://api.x.ai/v1/codegen",
        headers={"Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"},
        json={"spec": open(spec_path).read()}
    )
    with open(f"{output_dir}/enhanced_client.py", "w") as f:
        f.write(response.json().get("code", "# Enhanced client code"))

def main():
    generate_openapi_client("services/auth-service/openapi.yaml", "services/auth-service/client")

if __name__ == "__main__":
    main()
