import axios from 'axios';

// Base URL configuration (e.g., https://smarthire-cfl3.onrender.com)
let rawBase = import.meta.env.VITE_API_URL || '';
// Strip trailing slashes and trailing /api if present
rawBase = rawBase.replace(/\/+$/, '').replace(/\/api$/, '');
const API_BASE_URL = rawBase;

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

    // DO NOT manually set Content-Type: multipart/form-data!
    // Axios & browser automatically set multipart/form-data with the boundary when passing FormData.
    const response = await apiClient.post('/api/analyze-resume', formData);

    return response.data;
  } catch (error) {
    console.error('API analyzeResume error:', error);
    if (error.code === 'ECONNABORTED' || (error.message && error.message.includes('timeout'))) {
      throw new Error('Analysis request timed out. Please ensure the backend server is active.');
    } else if (error.response) {
      // Server responded with non-2xx status
      const backendMessage = error.response.data?.detail || error.response.data?.message || `Server error (${error.response.status})`;
      throw new Error(`Resume analysis failed: ${backendMessage}`);
    } else if (error.request) {
      // Request made but no response received (Backend server down or unreachable)
      throw new Error('Backend could not be reached. Please check your network or ensure the backend server is active.');
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
