"""
CyberRotate Pro - Database Manager
Enterprise database management with SQLite and PostgreSQL support
"""

import sqlite3
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging
from contextlib import asynccontextmanager

try:
    import asyncpg
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

try:
    import aiosqlite
    SQLITE_ASYNC_AVAILABLE = True
except ImportError:
    SQLITE_ASYNC_AVAILABLE = False

class DatabaseManager:
    """Enterprise database management system"""
    
    def __init__(self, database_url: str = None, pool_size: int = 10):
        self.database_url = database_url or "sqlite:///data/cyberrotate.db"
        self.pool_size = pool_size
        self.connection_pool = None
        self.db_type = self._detect_db_type()
        self.logger = logging.getLogger(__name__)
        
        # Note: initialize_database() should be called explicitly in async context
    
    def _detect_db_type(self) -> str:
        """Detect database type from URL"""
        if self.database_url.startswith("postgresql://") or self.database_url.startswith("postgres://"):
            return "postgresql"
        elif self.database_url.startswith("sqlite://"):
            return "sqlite"
        else:
            return "sqlite"  # Default fallback
    
    async def initialize_database(self):
        """Initialize database schema"""
        if self.db_type == "postgresql":
            await self._init_postgresql()
        else:
            await self._init_sqlite()
    
    async def _init_postgresql(self):
        """Initialize PostgreSQL database"""
        if not POSTGRESQL_AVAILABLE:
            raise Exception("PostgreSQL support requires asyncpg: pip install asyncpg")
        
        # Extract connection parameters
        url_parts = self.database_url.replace("postgresql://", "").replace("postgres://", "")
        
        try:
            # Create connection pool
            self.connection_pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=self.pool_size
            )
            
            # Create schema
            await self._create_postgresql_schema()
            self.logger.info("PostgreSQL database initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize PostgreSQL: {e}")
            # Fallback to SQLite
            self.db_type = "sqlite"
            await self._init_sqlite()
    
    async def _init_sqlite(self):
        """Initialize SQLite database"""
        # Extract path from SQLite URL
        db_path = self.database_url.replace("sqlite:///", "").replace("sqlite://", "")
        
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        if SQLITE_ASYNC_AVAILABLE:
            # Use async SQLite
            self.connection_pool = db_path
            await self._create_sqlite_schema()
        else:
            # Use sync SQLite
            self.connection_pool = db_path
            self._create_sqlite_schema_sync()
        
        self.logger.info(f"SQLite database initialized: {db_path}")
    
    async def _create_postgresql_schema(self):
        """Create PostgreSQL database schema"""
        schema_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            api_key VARCHAR(255) UNIQUE,
            role VARCHAR(50) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT true
        );
        
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            session_id VARCHAR(255) UNIQUE NOT NULL,
            ip_address INET,
            location_country VARCHAR(100),
            location_city VARCHAR(100),
            service_type VARCHAR(50),
            provider VARCHAR(100),
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            data_transferred BIGINT DEFAULT 0,
            status VARCHAR(50) DEFAULT 'active'
        );
        
        -- Connections table
        CREATE TABLE IF NOT EXISTS connections (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES sessions(id),
            connection_type VARCHAR(50) NOT NULL,
            server_name VARCHAR(100),
            server_country VARCHAR(100),
            server_ip INET,
            local_ip INET,
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            disconnected_at TIMESTAMP,
            duration INTEGER,
            bytes_sent BIGINT DEFAULT 0,
            bytes_received BIGINT DEFAULT 0,
            success BOOLEAN DEFAULT true,
            error_message TEXT
        );
        
        -- Analytics table
        CREATE TABLE IF NOT EXISTS analytics (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            event_type VARCHAR(100) NOT NULL,
            event_data JSONB,
            ip_address INET,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- System logs table
        CREATE TABLE IF NOT EXISTS system_logs (
            id SERIAL PRIMARY KEY,
            level VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            module VARCHAR(100),
            user_id INTEGER REFERENCES users(id),
            ip_address INET,
            metadata JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- API usage table
        CREATE TABLE IF NOT EXISTS api_usage (
            id SERIAL PRIMARY KEY,
            api_key VARCHAR(255),
            endpoint VARCHAR(255) NOT NULL,
            method VARCHAR(10) NOT NULL,
            status_code INTEGER,
            response_time FLOAT,
            ip_address INET,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time);
        CREATE INDEX IF NOT EXISTS idx_connections_session_id ON connections(session_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics(user_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp);
        CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);
        CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);
        """
        
        async with self.connection_pool.acquire() as conn:
            await conn.execute(schema_sql)
    
    async def _create_sqlite_schema(self):
        """Create SQLite database schema (async)"""
        schema_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        );
        
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            session_id TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            location_country TEXT,
            location_city TEXT,
            service_type TEXT,
            provider TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            data_transferred INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active'
        );
        
        -- Connections table
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER REFERENCES sessions(id),
            connection_type TEXT NOT NULL,
            server_name TEXT,
            server_country TEXT,
            server_ip TEXT,
            local_ip TEXT,
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            disconnected_at TIMESTAMP,
            duration INTEGER,
            bytes_sent INTEGER DEFAULT 0,
            bytes_received INTEGER DEFAULT 0,
            success BOOLEAN DEFAULT 1,
            error_message TEXT
        );
        
        -- Analytics table
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            event_type TEXT NOT NULL,
            event_data TEXT,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- System logs table
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            module TEXT,
            user_id INTEGER REFERENCES users(id),
            ip_address TEXT,
            metadata TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- API usage table
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time);
        CREATE INDEX IF NOT EXISTS idx_connections_session_id ON connections(session_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics(user_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp);
        CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);
        CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);
        """
        
        async with aiosqlite.connect(self.connection_pool) as conn:
            await conn.executescript(schema_sql)
            await conn.commit()
    
    def _create_sqlite_schema_sync(self):
        """Create SQLite database schema (sync)"""
        schema_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        );
        
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            session_id TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            location_country TEXT,
            location_city TEXT,
            service_type TEXT,
            provider TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            data_transferred INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active'
        );
        
        -- Connections table
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER REFERENCES sessions(id),
            connection_type TEXT NOT NULL,
            server_name TEXT,
            server_country TEXT,
            server_ip TEXT,
            local_ip TEXT,
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            disconnected_at TIMESTAMP,
            duration INTEGER,
            bytes_sent INTEGER DEFAULT 0,
            bytes_received INTEGER DEFAULT 0,
            success BOOLEAN DEFAULT 1,
            error_message TEXT
        );
        
        -- Analytics table
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            event_type TEXT NOT NULL,
            event_data TEXT,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- System logs table
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            module TEXT,
            user_id INTEGER REFERENCES users(id),
            ip_address TEXT,
            metadata TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- API usage table
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with sqlite3.connect(self.connection_pool) as conn:
            conn.executescript(schema_sql)
            conn.commit()
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if self.db_type == "postgresql":
            async with self.connection_pool.acquire() as conn:
                yield conn
        else:
            if SQLITE_ASYNC_AVAILABLE:
                async with aiosqlite.connect(self.connection_pool) as conn:
                    yield conn
            else:
                # Sync SQLite connection (wrapped to look async)
                with sqlite3.connect(self.connection_pool) as conn:
                    conn.row_factory = sqlite3.Row
                    yield conn
    
    async def create_user(self, username: str, email: str, password_hash: str, role: str = "user") -> int:
        """Create a new user"""
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                result = await conn.fetchrow(
                    "INSERT INTO users (username, email, password_hash, role) VALUES ($1, $2, $3, $4) RETURNING id",
                    username, email, password_hash, role
                )
                return result['id']
            else:
                if SQLITE_ASYNC_AVAILABLE:
                    cursor = await conn.execute(
                        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                        (username, email, password_hash, role)
                    )
                    await conn.commit()
                    return cursor.lastrowid
                else:
                    cursor = conn.execute(
                        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                        (username, email, password_hash, role)
                    )
                    conn.commit()
                    return cursor.lastrowid
    
    async def get_user_by_api_key(self, api_key: str) -> Optional[Dict]:
        """Get user by API key"""
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                result = await conn.fetchrow("SELECT * FROM users WHERE api_key = $1", api_key)
                return dict(result) if result else None
            else:
                if SQLITE_ASYNC_AVAILABLE:
                    cursor = await conn.execute("SELECT * FROM users WHERE api_key = ?", (api_key,))
                    result = await cursor.fetchone()
                else:
                    cursor = conn.execute("SELECT * FROM users WHERE api_key = ?", (api_key,))
                    result = cursor.fetchone()
                
                return dict(result) if result else None
    
    async def create_session(self, user_id: int, session_id: str, **kwargs) -> int:
        """Create a new session"""
        fields = ["user_id", "session_id"]
        values = [user_id, session_id]
        placeholders = ["$1", "$2"] if self.db_type == "postgresql" else ["?", "?"]
        
        # Add optional fields
        for i, (key, value) in enumerate(kwargs.items(), start=3):
            fields.append(key)
            values.append(value)
            placeholders.append(f"${i}" if self.db_type == "postgresql" else "?")
        
        query = f"INSERT INTO sessions ({', '.join(fields)}) VALUES ({', '.join(placeholders)}) RETURNING id"
        
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                result = await conn.fetchrow(query, *values)
                return result['id']
            else:
                if SQLITE_ASYNC_AVAILABLE:
                    cursor = await conn.execute(
                        query.replace(" RETURNING id", ""),
                        values
                    )
                    await conn.commit()
                    return cursor.lastrowid
                else:
                    cursor = conn.execute(
                        query.replace(" RETURNING id", ""),
                        values
                    )
                    conn.commit()
                    return cursor.lastrowid
    
    async def log_analytics_event(self, user_id: int, event_type: str, event_data: Dict = None, **kwargs):
        """Log analytics event"""
        event_data_json = json.dumps(event_data) if event_data else None
        
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                await conn.execute(
                    "INSERT INTO analytics (user_id, event_type, event_data, ip_address, user_agent) VALUES ($1, $2, $3, $4, $5)",
                    user_id, event_type, event_data, kwargs.get('ip_address'), kwargs.get('user_agent')
                )
            else:
                if SQLITE_ASYNC_AVAILABLE:
                    await conn.execute(
                        "INSERT INTO analytics (user_id, event_type, event_data, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)",
                        (user_id, event_type, event_data_json, kwargs.get('ip_address'), kwargs.get('user_agent'))
                    )
                    await conn.commit()
                else:
                    conn.execute(
                        "INSERT INTO analytics (user_id, event_type, event_data, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)",
                        (user_id, event_type, event_data_json, kwargs.get('ip_address'), kwargs.get('user_agent'))
                    )
                    conn.commit()
    
    async def get_usage_stats(self, user_id: int = None, days: int = 30) -> Dict:
        """Get usage statistics"""
        since_date = datetime.now() - timedelta(days=days)
        
        base_query = """
        SELECT 
            COUNT(*) as total_sessions,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_sessions,
            SUM(data_transferred) as total_data,
            AVG(EXTRACT(EPOCH FROM (end_time - start_time))) as avg_duration
        FROM sessions 
        WHERE start_time >= %s
        """
        
        if user_id:
            base_query += " AND user_id = %s"
            params = [since_date, user_id]
        else:
            params = [since_date]
        
        # Adjust query for SQLite
        if self.db_type == "sqlite":
            base_query = base_query.replace("EXTRACT(EPOCH FROM (end_time - start_time))", 
                                          "(julianday(end_time) - julianday(start_time)) * 86400")
            base_query = base_query.replace("%s", "?")
        
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                result = await conn.fetchrow(base_query, *params)
            else:
                if SQLITE_ASYNC_AVAILABLE:
                    cursor = await conn.execute(base_query, params)
                    result = await cursor.fetchone()
                else:
                    cursor = conn.execute(base_query, params)
                    result = cursor.fetchone()
            
            return dict(result) if result else {}
    
    async def cleanup_old_data(self, days: int = 90):
        """Clean up old data"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cleanup_queries = [
            "DELETE FROM system_logs WHERE timestamp < %s",
            "DELETE FROM api_usage WHERE timestamp < %s",
            "DELETE FROM analytics WHERE timestamp < %s"
        ]
        
        if self.db_type == "sqlite":
            cleanup_queries = [q.replace("%s", "?") for q in cleanup_queries]
        
        async with self.get_connection() as conn:
            for query in cleanup_queries:
                if self.db_type == "postgresql":
                    await conn.execute(query, cutoff_date)
                else:
                    if SQLITE_ASYNC_AVAILABLE:
                        await conn.execute(query, (cutoff_date,))
                    else:
                        conn.execute(query, (cutoff_date,))
            
            if self.db_type == "sqlite" and not SQLITE_ASYNC_AVAILABLE:
                conn.commit()

# Global database manager instance
db_manager = None

def get_database_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager

if __name__ == "__main__":
    # Test database manager
    async def test_db():
        db = DatabaseManager()
        await db.initialize_database()
        
        # Test user creation
        user_id = await db.create_user("testuser", "test@example.com", "hashed_password")
        print(f"Created user with ID: {user_id}")
        
        # Test session creation
        session_id = await db.create_session(user_id, "test_session_123", ip_address="192.168.1.1")
        print(f"Created session with ID: {session_id}")
        
        # Test analytics
        await db.log_analytics_event(user_id, "connection_started", {"server": "us-east-1"})
        print("Logged analytics event")
        
        # Test stats
        stats = await db.get_usage_stats(user_id)
        print(f"Usage stats: {stats}")
    
    asyncio.run(test_db())
