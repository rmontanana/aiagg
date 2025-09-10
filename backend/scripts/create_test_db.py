#!/usr/bin/env python3
"""
Script to create the test database for integration tests.
Run this before running integration tests.
"""

import asyncio
import asyncpg
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import sys


async def create_test_database():
    """Create the test database if it doesn't exist."""
    try:
        # Connect to postgres database to create the test database
        conn = await asyncpg.connect(
            user="postgres",
            password="postgres", 
            host="localhost",
            port=5432,
            database="postgres"
        )
        
        # Check if test database exists
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 'aiagg_test'"
        )
        
        if not result:
            print("Creating test database 'aiagg_test'...")
            await conn.execute("CREATE DATABASE aiagg_test")
            print("✅ Test database created successfully!")
        else:
            print("✅ Test database 'aiagg_test' already exists")
            
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error creating test database: {e}")
        print("\n💡 Make sure PostgreSQL is running:")
        print("   docker-compose up -d db")
        sys.exit(1)


def create_test_database_sync():
    """Synchronous version using SQLAlchemy."""
    try:
        # Connect to postgres database
        engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
        
        with engine.connect() as conn:
            # Set autocommit for database creation
            conn.execution_options(autocommit=True)
            
            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = 'aiagg_test'")
            ).fetchone()
            
            if not result:
                print("Creating test database 'aiagg_test'...")
                conn.execute(text("CREATE DATABASE aiagg_test"))
                print("✅ Test database created successfully!")
            else:
                print("✅ Test database 'aiagg_test' already exists")
                
    except Exception as e:
        print(f"❌ Error creating test database: {e}")
        print("\n💡 Make sure PostgreSQL is running:")
        print("   docker-compose up -d db")
        sys.exit(1)


if __name__ == "__main__":
    print("🔧 Setting up test database...")
    try:
        # Try async version first
        asyncio.run(create_test_database())
    except ImportError:
        # Fall back to sync version
        create_test_database_sync()
    
    print("\n🧪 Ready to run integration tests!")
    print("   export ENVIRONMENT=test")
    print("   uv run pytest tests/test_integration.py -v")