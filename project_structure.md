# PersonableCRM - Complete Project Structure

## Directory Tree

```
lux-crm/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── config.py                 # Configuration and environment variables
│   │   ├── db.py                     # Database setup and session management
│   │   ├── models.py                 # SQLAlchemy ORM models
│   │   ├── schemas.py                # Pydantic schemas for validation
│   │   │
│   │   ├── lux/                      # Lux AI integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py             # Lux client singleton
│   │   │   ├── agents.py             # Agent instruction templates
│   │   │   └── tasks.py              # Task execution and parsing
│   │   │
│   │   ├── services/                 # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── crm.py                # Contact CRUD operations
│   │   │   └── research.py           # Research orchestration
│   │   │
│   │   └── routes/                   # API endpoints
│   │       ├── __init__.py
│   │       ├── contacts.py           # Contact management routes
│   │       └── research.py           # Research task routes
│   │
│   ├── Dockerfile                    # Backend Docker configuration
│   ├── requirements.txt              # Python dependencies
│   └── crm.db                        # SQLite database (gitignored)
│
├── frontend/                         # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx                # Root layout with metadata
│   │   ├── page.tsx                  # Home page - research interface
│   │   ├── globals.css               # Global styles
│   │   │
│   │   └── contacts/
│   │       └── page.tsx              # Contacts list page
│   │
│   ├── Dockerfile                    # Frontend Docker configuration
│   ├── package.json                  # Node dependencies
│   ├── next.config.js                # Next.js configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   └── tsconfig.json                 # TypeScript configuration
│
├── docker-compose.yml                # Multi-container orchestration
├── .env.example                      # Environment variables template
├── .env                              # Actual environment variables (gitignored)
├── .gitignore                        # Git ignore rules
├── setup.sh                          # Setup automation script
├── README.md                         # Main documentation
└── PROJECT_STRUCTURE.md              # This file
```

## File Descriptions

### Backend Files

#### Core Application
- **`main.py`**: FastAPI app initialization, middleware, route registration, startup/shutdown events
- **`config.py`**: Environment variables, API keys, database URLs, CORS settings
- **`db.py`**: SQLAlchemy engine, session factory, database dependency for routes

#### Data Layer
- **`models.py`**: 
  - `Contact`: People discovered through research
  - `Conversation`: Email threads and interactions
  - `ResearchSource`: Tracking where contacts were found
  - `ResearchTask`: Status and results of agent tasks

- **`schemas.py`**: Pydantic models for request/response validation and serialization

#### Lux Integration
- **`lux/client.py`**: Singleton Lux agent instance with API key management
- **`lux/agents.py`**: Instruction templates for people research and enrichment
- **`lux/tasks.py`**: Execute agent tasks, parse JSON responses, validate contact data

#### Business Logic
- **`services/crm.py`**: 
  - Contact CRUD operations
  - Conversation management
  - Research source tracking
  - Bulk operations with duplicate handling

- **`services/research.py`**:
  - Orchestrate Lux agent research
  - Create research task records
  - Validate and store results
  - Link sources to contacts

#### API Routes
- **`routes/contacts.py`**:
  - `GET /api/contacts` - List contacts with pagination
  - `GET /api/contacts/search` - Search functionality
  - `GET /api/contacts/{id}` - Contact details with relations
  - `POST /api/contacts` - Create contact manually
  - `PUT /api/contacts/{id}` - Update contact
  - `DELETE /api/contacts/{id}` - Delete contact
  - Conversation endpoints

- **`routes/research.py`**:
  - `POST /api/research` - Start async research task
  - `POST /api/research/sync` - Synchronous research
  - `GET /api/research/tasks` - List all tasks
  - `GET /api/research/tasks/{id}` - Task details

### Frontend Files

#### Pages
- **`app/page.tsx`**: Main research interface with query input and task submission
- **`app/contacts/page.tsx`**: Contact list with search, view, and delete functionality
- **`app/layout.tsx`**: Root layout with metadata and global styles

#### Configuration
- **`next.config.js`**: API proxy configuration for development
- **`tailwind.config.js`**: Tailwind CSS customization
- **`package.json`**: Dependencies and scripts

### Infrastructure Files

- **`docker-compose.yml`**: Orchestrates backend and frontend containers with networking
- **`Dockerfile`** (backend): Python environment, dependencies, uvicorn server
- **`Dockerfile`** (frontend): Node.js environment, Next.js dev server
- **`setup.sh`**: Automated setup script for local development
- **`.env.example`**: Template for required environment variables
- **`.gitignore`**: Excludes sensitive files, dependencies, build artifacts

## Data Flow

### Research Flow
```
User Input (Frontend)
    ↓
POST /api/research
    ↓
research.py service
    ↓
Lux Agent Execution
    ↓
JSON Response Parsing
    ↓
Contact Validation
    ↓
Bulk Insert (crm.py)
    ↓
Source Linking
    ↓
Task Status Update
```

### Contact Display Flow
```
Frontend Request
    ↓
GET /api/contacts
    ↓
contacts.py route
    ↓
crm.py service
    ↓
SQLAlchemy Query
    ↓
Pydantic Serialization
    ↓
JSON Response
    ↓
Frontend Rendering
```

## Key Design Patterns

### Backend Architecture
- **Layered Architecture**: Routes → Services → Models
- **Dependency Injection**: Database sessions via FastAPI Depends
- **Singleton Pattern**: Lux client instance
- **Repository Pattern**: CRM service abstracts data access

### Error Handling
- **Validation**: Pydantic schemas at API boundary
- **Try-Catch**: Service layer catches and logs exceptions
- **HTTP Exceptions**: Routes return appropriate status codes
- **Background Tasks**: Research runs async to avoid timeouts

### Database Design
- **Normalization**: Separate tables for contacts, conversations, sources
- **Relationships**: Foreign keys with cascading deletes
- **Indexes**: Email uniqueness, ID lookups
- **Timestamps**: Track creation and updates

## Extension Points

### Adding New Agent Capabilities
1. Add instruction template to `lux/agents.py`
2. Create execution function in `lux/tasks.py`
3. Add service method in appropriate service file
4. Create route in routes directory

### Adding New Data Models
1. Define model in `models.py`
2. Create schemas in `schemas.py`
3. Add CRUD operations to service
4. Create API routes
5. Update frontend to consume new endpoints

### Adding Frontend Pages
1. Create new directory in `app/`
2. Add `page.tsx` component
3. Update navigation in main pages
4. Make API calls to backend

## Environment Variables Reference

```env
# Required
LUX_API_KEY=<your-lux-api-key>

# Optional with defaults
LUX_MODEL=lux-thinker-1
DATABASE_URL=sqlite:///./crm.db
APP_NAME=PersonableCRM
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Development Workflow

1. **Start Development**:
   ```bash
   docker-compose up
   # OR manually start backend and frontend
   ```

2. **Make Changes**:
   - Backend changes auto-reload with uvicorn `--reload`
   - Frontend changes hot-reload with Next.js dev server

3. **Test API**:
   - Visit `http://localhost:8000/docs` for interactive API docs
   - Use Postman/curl for manual testing

4. **View Logs**:
   - Docker: `docker-compose logs -f`
   - Manual: Check terminal outputs

## Production Considerations

### Database
- Migrate from SQLite to PostgreSQL
- Add database migrations with Alembic
- Set up connection pooling

### Security
- Add authentication (JWT tokens)
- Implement rate limiting
- Use HTTPS only
- Validate and sanitize all inputs
- Store API keys in secrets manager

### Performance
- Add caching (Redis)
- Implement pagination properly
- Use async database operations
- Add CDN for frontend assets

### Monitoring
- Add logging aggregation
- Set up error tracking (Sentry)
- Implement health checks
- Monitor API performance

---

This structure is designed to be:
- **Scalable**: Easy to add new features
- **Maintainable**: Clear separation of concerns
- **Testable**: Services can be unit tested
- **Deployable**: Docker-ready for any environment