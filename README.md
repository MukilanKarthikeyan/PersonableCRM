# PersonableCRM

A personal CRM system powered by Lux AI for intelligent people research and outreach management.

## Features

- 🤖 **AI-Powered Research**: Use Lux (OpenAGI) to automatically discover and extract contact information
- 👥 **Contact Management**: Store and organize people with rich metadata (affiliation, field, website)
- 💬 **Conversation Tracking**: Keep track of email threads and outreach status
- 🔍 **Smart Search**: Search contacts by name, email, affiliation, or field
- 📊 **Research Tasks**: Monitor the status and results of AI research tasks
- 🌐 **Source Tracking**: Know where each contact was discovered

## Architecture

```
lux-crm/
├── backend/          # FastAPI + SQLAlchemy + Lux
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── lux/
│   │   │   ├── client.py
│   │   │   ├── agents.py
│   │   │   └── tasks.py
│   │   ├── services/
│   │   │   ├── crm.py
│   │   │   └── research.py
│   │   └── routes/
│   │       ├── contacts.py
│   │       └── research.py
│   └── requirements.txt
│
├── frontend/         # Next.js + TypeScript + Tailwind
│   ├── app/
│   │   ├── page.tsx
│   │   ├── contacts/
│   │   └── layout.tsx
│   └── package.json
│
└── docker-compose.yml
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- Lux API Key from OpenAGI

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd lux-crm
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your Lux API key:

```env
LUX_API_KEY=your_lux_api_key_here
LUX_MODEL=lux-thinker-1
DATABASE_URL=sqlite:///./crm.db
DEBUG=True
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

This will start:
- Backend API at `http://localhost:8000`
- Frontend at `http://localhost:3000`
- API docs at `http://localhost:8000/docs`

### 4. Run Locally (Alternative)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Usage

### 1. Start a Research Task

Visit `http://localhost:3000` and enter a research query like:

- "robotics professors at MIT"
- "AI researchers working on computer vision"
- "machine learning engineers at Google"

The Lux agent will:
1. Search the web for relevant people
2. Visit their pages and extract contact info
3. Validate and store results in your CRM

### 2. View Contacts

Navigate to the Contacts page to see all discovered people. Each contact includes:
- Name and email
- Affiliation and field
- Personal website
- Source URL (where they were found)

### 3. Track Conversations

For each contact, you can:
- Create conversation threads
- Track email status (draft, sent, replied, follow-up)
- Add notes and context

## API Endpoints

### Research
- `POST /api/research` - Start a new research task (async)
- `POST /api/research/sync` - Start a research task (synchronous)
- `GET /api/research/tasks` - List all research tasks
- `GET /api/research/tasks/{id}` - Get specific task details

### Contacts
- `GET /api/contacts` - List all contacts
- `GET /api/contacts/search?q=query` - Search contacts
- `GET /api/contacts/{id}` - Get contact details
- `POST /api/contacts` - Create contact manually
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact

### Conversations
- `POST /api/contacts/{id}/conversations` - Create conversation
- `GET /api/contacts/{id}/conversations` - List conversations
- `PATCH /api/conversations/{id}/status` - Update status

Full API documentation available at: `http://localhost:8000/docs`

## Database Schema

### Contact
- `id`, `name`, `email` (unique)
- `affiliation`, `field`, `website`
- `source_url`, `confidence`
- `created_at`, `updated_at`

### Conversation
- `id`, `contact_id`
- `subject`, `body`, `status`
- `sent_at`, `created_at`

### ResearchSource
- `id`, `contact_id`
- `url`, `extracted_at`, `extraction_method`

### ResearchTask
- `id`, `query`, `status`
- `results_count`, `error_message`
- `created_at`, `completed_at`

## Development

### Backend Testing
```bash
cd backend
pytest
```

### Adding New Agent Instructions

Edit `backend/app/lux/agents.py` to customize:
- Research instructions
- Extraction logic
- Enrichment behavior

### Modifying Database Schema

```bash
cd backend
# Create migration
alembic revision --autogenerate -m "description"
# Apply migration
alembic upgrade head
```

## Production Deployment

### Environment Variables

```env
LUX_API_KEY=<your-production-key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DEBUG=False
LOG_LEVEL=INFO
```

### Security Considerations

1. **Never commit** your `.env` file
2. Use **PostgreSQL** instead of SQLite in production
3. Enable **HTTPS** for frontend
4. Add **rate limiting** to API endpoints
5. Implement **authentication** for multi-user scenarios

## Legal & Ethical Considerations

⚠️ **Important**: This tool is designed for professional outreach only.

- Only extracts **publicly listed** contact information
- Stores **source URLs** for transparency
- Respects **robots.txt** during web scraping
- Complies with **CAN-SPAM** and **GDPR** requirements

**Best Practices:**
- Use for academic/professional networking only
- Always include opt-out mechanisms in emails
- Respect privacy and consent
- Don't scrape personal social media
- Limit outreach frequency

## Troubleshooting

### Lux API Errors
- Verify your API key is correct
- Check OpenAGI service status
- Review agent logs in backend console

### Database Issues
- Delete `crm.db` and restart to reset
- Check file permissions
- For production, use PostgreSQL

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS_ORIGINS in config.py
- Verify frontend calls correct API URL

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Lux (OpenAGI)](https://openagi.com/)
- Frontend with [Next.js](https://nextjs.org/)
- UI styled with [Tailwind CSS](https://tailwindcss.com/)

## Support

For issues or questions:
- Open an issue on GitHub
- Check API docs at `/docs`
- Review agent logs for debugging

---

**Built with ❤️ for better professional networking**