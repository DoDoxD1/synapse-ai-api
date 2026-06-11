"""
Script to create .env file from .env.example with user prompts
"""
import os
import secrets

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file interactively"""
    print("🔧 Synapse AI Backend - Environment Setup\n")
    
    # Load .env.example
    example_file = os.path.join(os.path.dirname(__file__), '..', '.env.example')
    
    if not os.path.exists(example_file):
        print("❌ .env.example file not found!")
        return
    
    with open(example_file, 'r') as f:
        content = f.read()
    
    # Generate secret key
    secret_key = generate_secret_key()
    content = content.replace('your-super-secret-key-change-this-in-production', secret_key)
    
    # Get OpenAI API key
    print("Enter your OpenAI API key (or press Enter to skip):")
    openai_key = input("OPENAI_API_KEY: ").strip()
    
    if openai_key:
        content = content.replace('sk-your-openai-api-key-here', openai_key)
    
    # Get database configuration
    print("\nDatabase Configuration (press Enter for defaults):")
    db_user = input("Database User [synapse]: ").strip() or "synapse"
    db_pass = input("Database Password [password]: ").strip() or "password"
    db_host = input("Database Host [localhost]: ").strip() or "localhost"
    db_port = input("Database Port [5432]: ").strip() or "5432"
    db_name = input("Database Name [synapse_db]: ").strip() or "synapse_db"
    
    db_url = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    content = content.replace('postgresql+asyncpg://synapse:password@localhost:5432/synapse_db', db_url)
    
    # Write .env file
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"\n✅ .env file created successfully!")
    print(f"📍 Location: {os.path.abspath(env_file)}")
    print("\n⚠️  Remember to:")
    print("   1. Set your OPENAI_API_KEY in .env if you skipped it")
    print("   2. Ensure PostgreSQL and Redis are running")
    print("   3. Run 'alembic upgrade head' to create database tables")

if __name__ == "__main__":
    create_env_file()
