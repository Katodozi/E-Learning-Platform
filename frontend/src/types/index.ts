export interface User {
  id: number;
  email: string;
  selected_expertise: string | null;
  selected_roadmap: number | null;
}

export interface Expertise {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
}

export interface RoadmapSummary {
  id: number;
  title: string;
  level: string;
  description: string;
  estimated_duration: string;
  skill_count: number;
}

export interface SkillSummary {
  id: number;
  name: string;
  description: string;
  order_index: number;
  topic_count: number;
}

export interface RoadmapDetail {
  id: number;
  title: string;
  level: string;
  description: string;
  estimated_duration: string;
  expertise_id: number;
  expertise_name: string;
  skills: SkillSummary[];
}

export interface Topic {
  id: number;
  name: string;
  description: string;
  order_index: number;
  completed: boolean;
}

export interface SkillContent {
  skill_id: number;
  skill_name: string;
  overview: string;
  core_concepts: string;
  basic_explanation: string;
  real_world_example: string;
  summary: string;
  topics: Topic[];
  cached: boolean;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
}

export interface QuizResult {
  skill_id: number;
  score: number;
  proficiency: string;
  correct_count: number;
  total_questions: number;
  results: Array<{
    question: string;
    your_answer: number;
    correct_answer: number;
    is_correct: boolean;
    explanation: string;
  }>;
}

export interface DashboardData {
  selected_roadmap: {
    id: number;
    title: string;
    level: string;
    expertise_name: string;
    estimated_duration: string;
  } | null;
  overall_completion: number;
  completed_skills: number;
  remaining_skills: number;
  total_skills: number;
  quiz_scores: Array<{ quiz_id: number; score: number; attempted_at: string }>;
  current_streak: number;
  recently_completed_topics: Array<{ topic_id: number; topic_name: string; completed_at: string | null }>;
  progress_chart: Array<{ date: string; topics_completed: number }>;
  skill_progress: Array<{
    skill_id: number;
    skill_name: string;
    topics_completed: number;
    topics_total: number;
    topic_progress: number;
    quiz_score: number | null;
    completed: boolean;
  }>;
}

export interface PromptTemplate {
  id: number;
  name: string;
  prompt_type: string;
  template: string;
  is_active: boolean;
}

export interface Analytics {
  total_users: number;
  total_expertise: number;
  total_roadmaps: number;
  total_skills: number;
  total_quiz_attempts: number;
  average_quiz_score: number;
  active_users_last_7_days: number;
}

export interface UserProgressSummary {
  id: number;
  email: string;
  selected_expertise: string | null;
  selected_roadmap: number | null;
  completed_skills: number;
  overall_completion: number;
}

export interface AuthContext {
  selectedExpertise?: string;
  selectedRoadmap?: number;
}
