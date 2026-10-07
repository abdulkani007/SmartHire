import axios from 'axios';

// Defaults to relative URL '' to leverage Vite proxy, or env variable if defined
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
  },
  timeout: 120000, // 120s timeout for heavy ML model execution over 148k jobs
});

/**
 * Uploads a resume file (PDF/DOCX/TXT) to the backend /api/analyze-resume endpoint.
 * @param {File} file - Resume file object
 */
export const analyzeResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/api/analyze-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED' || (error.message && error.message.includes('timeout'))) {
      throw new Error('Analysis request timed out. Please ensure the FastAPI backend server is active and try again.');
    } else if (error.response) {
      // Server responded with non-2xx status
      throw new Error(error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`);
    } else if (error.request) {
      // Request made but no response received (Backend server down or unreachable)
      throw new Error('Backend server is unreachable. Please ensure the FastAPI server is running on port 8000.');
    } else {
      throw new Error(error.message || 'Failed to submit resume for analysis.');
    }
  }
};

/**
 * Direct JSON endpoints
 */
export const predictCategory = async (resumeText) => {
  const response = await apiClient.post('/api/predict-category', { resume_text: resumeText });
  return response.data;
};

export const recommendJobs = async (resumeText, topN = 10) => {
  const response = await apiClient.post('/api/recommend-jobs', { resume_text: resumeText, top_n: topN });
  return response.data;
};

export const generateSkillGap = async (resumeText, targetCategory = null, topNSkills = 20) => {
  const response = await apiClient.post('/api/skill-gap', {
    resume_text: resumeText,
    target_category: targetCategory,
    top_n_skills: topNSkills,
  });
  return response.data;
};

export default apiClient;
