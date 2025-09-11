
# Intervista – AI-Powered Interview Preparation Platform

A brief description of what this project does and who it's for



## Acknowledgements  

This project was inspired by the challenges job seekers face in technical interview preparation.  
Special thanks to:  

- **[OpenAI](https://openai.com/)** for providing the powerful GPT API that enables intelligent question generation and feedback  
- **[Awesome README Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)** for documentation inspiration  
- **The Django and React communities** for their excellent documentation and support  
- **[Material-UI](https://mui.com/)** for the comprehensive component library that accelerated frontend development  
- **[Vite](https://vitejs.dev/)** for the fast and modern frontend build tooling  



##  Appendix  

Additional information and notes:  

- **Environment Variables**  
  Make sure to set up the required environment variables in a `.env` file:  
  - `OPENAI_API_KEY` → API key for GPT integration  
  - `DJANGO_SECRET_KEY` → Secret key for Django backend  
  - `DATABASE_URL` → (Optional) PostgreSQL connection string for production  

- **Demo Credentials (if applicable)**  
  You can provide test login credentials here once you deploy the project.  

- **Future Enhancements**  
  - Add support for behavioral interview questions  
  - Enable video interview simulations  
  - Expand job matching with LinkedIn/Indeed integration  

- **Known Limitations**  
  - Currently optimized for English only  
  - SQLite used in development (switch to PostgreSQL in production)
## 🚀 Deployment  

### Frontend (React + Vite)  
To build and deploy the frontend:  

```bash
# Build production files
cd frontend
npm run build

# Optional: Deploy to GitHub Pages / Vercel / Netlify
npm run deploy


## Backend (Django REST Framework)

cd backend
# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Start server (can use gunicorn / uvicorn)
gunicorn backend.wsgi



✨ Features  
- **AI Question Generator**: Generates role-specific technical interview questions using the backend (powered by OpenAI GPT API or fallback logic).  
- **Real-time Answer Evaluation**: Evaluates user answers and provides instant feedback.  
- **Role Selection**: Allows users to practice for a selected job role (if a job role selector is available).  
- **Session Reset**: Users can reset their session and start over.  
- **Loading Indicators**: Shows spinners while generating questions or evaluating answers.  
- **Error Handling**: Displays clear error messages if the backend or API fails.  
- **Material UI Design**: Modern, responsive interface built with Material-UI for a professional look and feel.  
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

