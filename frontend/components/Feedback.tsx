import React, { useEffect, useState } from 'react';
import { feedbackApi, type FeedbackCreate, type CaptchaResponse } from '../api';
import { Send, Loader2, CheckCircle, AlertCircle, Mail, User, MessageSquare, FileText, ShieldCheck, RefreshCw } from 'lucide-react';

export const Feedback: React.FC = () => {
  const [formData, setFormData] = useState<FeedbackCreate>({
    name: '',
    email: '',
    subject: '',
    message: '',
    captcha_id: '',
    captcha_answer: '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [captcha, setCaptcha] = useState<CaptchaResponse | null>(null);
  const [captchaLoading, setCaptchaLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    // Force uppercase for captcha input
    const processedValue = name === 'captcha_answer' ? value.toUpperCase() : value;
    setFormData((prev) => ({ ...prev, [name]: processedValue }));
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const loadCaptcha = async () => {
    try {
      setCaptchaLoading(true);
      const data = await feedbackApi.getCaptcha();
      setCaptcha(data);
      setFormData((prev) => ({
        ...prev,
        captcha_id: data.captcha_id,
        captcha_answer: '',
      }));
      if (error) setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load captcha');
    } finally {
      setCaptchaLoading(false);
    }
  };

  useEffect(() => {
    loadCaptcha();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    if (!formData.captcha_answer || !formData.captcha_id) {
      setError('請完成驗證碼');
      setLoading(false);
      return;
    }

    try {
      await feedbackApi.submitFeedback(formData);
      setSuccess(true);
      // Reset form
      setFormData({
        name: '',
        email: '',
        subject: '',
        message: '',
        captcha_id: '',
        captcha_answer: '',
      });
      setCaptcha(null);
      await loadCaptcha();
      // Clear success message after 5 seconds
      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white rounded-2xl shadow-lg border border-slate-100 p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-accent-500 to-purple-500 rounded-full mb-4">
            <MessageSquare className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-slate-900 mb-2">Get In Touch</h2>
          <p className="text-slate-600">
            We'd love to hear from you! Send us a message and we'll respond as soon as possible.
          </p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
            <div>
              <p className="text-green-800 font-semibold">Thank you for your feedback!</p>
              <p className="text-green-700 text-sm">We've received your message and will get back to you soon.</p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
            <div>
              <p className="text-red-800 font-semibold">Error</p>
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-2">
              <User className="w-4 h-4 inline mr-2" />
              Name *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-accent-500 transition-colors"
              placeholder="Your name"
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
              <Mail className="w-4 h-4 inline mr-2" />
              Email *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-accent-500 transition-colors"
              placeholder="your.email@example.com"
            />
          </div>

          {/* Subject */}
          <div>
            <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-2">
              <FileText className="w-4 h-4 inline mr-2" />
              Subject
            </label>
            <input
              type="text"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-accent-500 transition-colors"
              placeholder="What's this about?"
            />
          </div>

          {/* Message */}
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-2">
              <MessageSquare className="w-4 h-4 inline mr-2" />
              Message *
            </label>
            <textarea
              id="message"
              name="message"
              required
              rows={6}
              value={formData.message}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-accent-500 transition-colors resize-none"
              placeholder="Tell us what's on your mind..."
            />
          </div>

          {/* Captcha */}
          <div>
            <label htmlFor="captcha" className="block text-sm font-medium text-slate-700 mb-2">
              <ShieldCheck className="w-4 h-4 inline mr-2" />
              驗證碼 *
            </label>
            <div className="flex items-center gap-3">
              <div className="flex-1">
                <input
                  type="text"
                  id="captcha"
                  name="captcha_answer"
                  required
                  value={formData.captcha_answer}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent-500 focus:border-accent-500 transition-colors uppercase"
                  placeholder="請輸入圖中文字"
                  disabled={captchaLoading}
                  style={{ textTransform: 'uppercase' }}
                />
              </div>
              <div className="flex items-center gap-2">
                {captcha?.image_base64 ? (
                  <img
                    src={captcha.image_base64}
                    alt="captcha"
                    className="h-12 w-28 rounded border border-slate-300 object-contain bg-white"
                  />
                ) : (
                  <div className="h-12 w-28 flex items-center justify-center border border-slate-300 rounded text-slate-500 text-sm">
                    {captchaLoading ? '載入中...' : '無法載入'}
                  </div>
                )}
                <button
                  type="button"
                  onClick={loadCaptcha}
                  className="p-3 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50"
                  disabled={captchaLoading}
                  aria-label="Refresh captcha"
                >
                  <RefreshCw className={`w-5 h-5 ${captchaLoading ? 'animate-spin' : ''}`} />
                </button>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-6 bg-gradient-to-r from-accent-600 to-purple-600 hover:from-accent-500 hover:to-purple-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Sending...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Send Message
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
