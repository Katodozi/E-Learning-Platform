import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BookOpen, Flame, Target, Trophy } from 'lucide-react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { ProgressRing } from '@/components/ui/ProgressRing';
import { dashboardApi } from '@/services/api';
import { formatDate, getProficiencyColor } from '@/utils/cn';

export function DashboardPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => dashboardApi.get().then((r) => r.data),
  });

  if (isLoading) {
    return <div className="glass rounded-xl h-96 animate-pulse" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold">Learning Dashboard</h1>
        <p className="text-text-secondary">Track your progress and continue learning</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { icon: Target, label: 'Overall Progress', value: `${data?.overall_completion || 0}%`, color: 'text-primary' },
          { icon: BookOpen, label: 'Completed Skills', value: `${data?.completed_skills || 0}/${data?.total_skills || 0}`, color: 'text-accent' },
          { icon: Trophy, label: 'Remaining Skills', value: String(data?.remaining_skills || 0), color: 'text-secondary' },
          { icon: Flame, label: 'Current Streak', value: `${data?.current_streak || 0} days`, color: 'text-success' },
        ].map(({ icon: Icon, label, value, color }, i) => (
          <motion.div key={label} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
            <Card>
              <div className="flex items-center gap-3">
                <div className={`rounded-lg bg-surface p-2 ${color}`}>
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm text-text-secondary">{label}</p>
                  <p className="text-xl font-bold">{value}</p>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 flex flex-col items-center justify-center py-8">
          <ProgressRing value={data?.overall_completion || 0} label="Complete" />
          {data?.selected_roadmap && (
            <div className="mt-6 text-center">
              <Badge className="mb-2">{data.selected_roadmap.level}</Badge>
              <h3 className="font-semibold">{data.selected_roadmap.title}</h3>
              <p className="text-sm text-text-secondary">{data.selected_roadmap.expertise_name}</p>
              <Link to={`/roadmap/${data.selected_roadmap.id}`} className="mt-4 inline-block">
                <Button size="sm" variant="outline">View Roadmap</Button>
              </Link>
            </div>
          )}
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Weekly Activity</CardTitle>
            <CardDescription>Topics completed over the last 7 days</CardDescription>
          </CardHeader>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.progress_chart || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" tick={{ fill: '#CBD5E1', fontSize: 12 }} tickFormatter={(v) => v.slice(5)} />
                <YAxis tick={{ fill: '#CBD5E1', fontSize: 12 }} allowDecimals={false} />
                <Tooltip
                  contentStyle={{ background: '#1E293B', border: '1px solid #334155', borderRadius: 8 }}
                  labelStyle={{ color: '#F8FAFC' }}
                />
                <Bar dataKey="topics_completed" fill="#2563EB" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Skill Progress</CardTitle>
          </CardHeader>
          <div className="space-y-3">
            {data?.skill_progress?.length ? (
              data.skill_progress.map((skill) => (
                <div key={skill.skill_id} className="flex items-center justify-between gap-4 p-3 rounded-lg bg-surface/50">
                  <div className="min-w-0">
                    <p className="font-medium truncate">{skill.skill_name}</p>
                    <p className="text-xs text-text-secondary">
                      {skill.topics_completed}/{skill.topics_total} topics
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    {skill.quiz_score !== null && (
                      <span className={`text-sm font-medium ${getProficiencyColor(skill.quiz_score)}`}>
                        {skill.quiz_score}%
                      </span>
                    )}
                    {skill.completed && <Badge variant="success">Done</Badge>}
                    <Link to={`/skill/${skill.skill_id}`}>
                      <Button size="sm" variant="ghost">Continue</Button>
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-text-secondary text-sm">No skills in progress yet.</p>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <div className="space-y-3">
            {data?.recently_completed_topics?.length ? (
              data.recently_completed_topics.map((topic) => (
                <div key={topic.topic_id} className="flex items-center justify-between p-3 rounded-lg bg-surface/50">
                  <span className="text-sm">{topic.topic_name}</span>
                  <span className="text-xs text-text-secondary">
                    {topic.completed_at ? formatDate(topic.completed_at) : ''}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-text-secondary text-sm">Complete topics to see activity here.</p>
            )}
          </div>

          {data?.quiz_scores?.length ? (
            <div className="mt-6 pt-4 border-t border-border">
              <h4 className="text-sm font-medium mb-3">Recent Quiz Scores</h4>
              {data.quiz_scores.slice(0, 5).map((q) => (
                <div key={q.quiz_id} className="flex justify-between text-sm py-1">
                  <span className={getProficiencyColor(q.score)}>{q.score}%</span>
                  <span className="text-text-secondary">{formatDate(q.attempted_at)}</span>
                </div>
              ))}
            </div>
          ) : null}
        </Card>
      </div>
    </div>
  );
}
