/**
 * Feedback API Service
 * Handles feedback submission API calls
 */

import { apiClient } from './client';
import { API_ENDPOINTS } from './config';

export interface FeedbackCreate {
  name: string;
  email: string;
  subject?: string;
  message: string;
}

export interface FeedbackResponse {
  id: number;
  name: string;
  email: string;
  subject: string | null;
  message: string;
  is_read: boolean;
  created_at: string;
  updated_at: string;
}

export const feedbackApi = {
  /**
   * Submit feedback
   */
  submitFeedback: async (feedback: FeedbackCreate): Promise<FeedbackResponse> => {
    return apiClient.post<FeedbackResponse>(API_ENDPOINTS.FEEDBACK, feedback);
  },
};
